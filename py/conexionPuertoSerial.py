import serial, time
from flask import Markup, jsonify
from pysnmp.hlapi import *
from py.dbController import dbController
from py.lectura import Lectura
from py.util import generate_random_array
from bson.timestamp import Timestamp
from datetime import datetime
import datetime as dt



class ConexionTarjeta():
    def __init__(self, documento):
        db = dbController("cinderella25").getDb()
        self.tarjetaDb = documento
        self.codigo = documento["codigo"] + "\r"
        self.lineaDatos = 0

    
    def leer_tarjeta(self, conexion_real = False):

        if conexion_real == False:
            self.lineaDatos = generate_random_array(13)
            return
        
        serialMicro = serial.Serial(self.tarjetaDb["puerto"],9600, timeout=1)  #establece la comunicación por el puerto serial
        time.sleep(.2)

        serialMicro.write(self.codigo.encode("ascii")) 
        time.sleep(.2)

        while self.lineaDatos == 0:
            self.lineaDatos = serialMicro.readline().decode("ascii", errors="ignore")
            self.lineaDatos = self.lineaDatos.split(',')  # convierte la entrada en lista
        time.sleep(.1)
        

    def cumpleCondiciones(self, limite, logica, valor):
        result = {
            "status": "OK",
            "limite_NA" : False,
            "limite_NC" : False
        }
        if logica == 'NA'and valor > limite:
            result["limite_NA"] = True
            result["status"] = "ALERT"

        if logica == 'NC' and valor < limite:
            result["limite_NC"] = True
            result["status"] = "ALERT"
        
        return result

    def validacion_sensores(self):
        db = dbController("cinderella25").getDb()
        result = []

        for i, datoSp in enumerate(self.lineaDatos):
            for alarma in self.tarjetaDb["alarmasconfig"]:
                if i == int(alarma["epgID"]) and datoSp != "END\n":
                    slope = float(alarma["slope"])
                    offset = float(alarma["offset"])
                    valorEnt = (float(datoSp))/float(alarma["convVolts"])

                    valor = (float(valorEnt)-float(offset))/float(slope)
                    conf_alarmas = db["conf_alarmas"].find_one({"usado" : "si", "origen" : alarma["epgLabel"]})
                    hora_reg = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    lecturaSensor = {
                        'epgLabel': alarma["epgLabel"], 
                        'valor': valor,
                        "unidad" : alarma["unidad"],
                        "hora_reg" : hora_reg}
                    
                    db["lecturas_" + self.tarjetaDb["codigo"]].insert_one(lecturaSensor)
                    
                    query = {'epgLabel': {'$regex': alarma["epgLabel"]}}
                    projection = {'valor': 1, 'hora_reg': 1, '_id': 0}
                    objs = db["lecturas_" + self.tarjetaDb["codigo"]].find(query, projection).limit(50).sort('_id', +1)

                    lecturaSensor["historial"] = list(objs)
                    
                    lecturaSensor["texto_largo"] = conf_alarmas["texto_largo"]
                    result.append(lecturaSensor)
                    
                    
                    if self.cumpleCondiciones(float(conf_alarmas["limite"]), conf_alarmas["logica"], valor):
                        statusActual = 'ACTIVA'
                        almOid = conf_alarmas["oid_set"]

                    else:
                        statusActual = 'NORMAL'
                        almOid = conf_alarmas["oid_clear"]

                    statusAnterior = db["notificaciones"].find_one({"clave" : conf_alarmas["clave"]})
                    if statusAnterior:
                        if statusAnterior["status"] != statusActual:
                            for iptrap in self.tarjetaDb["iptrap"]:
                                self.enviaTrap(alarma, almOid, iptrap)
                                
                        db["notificaciones"].update_one({"clave" : conf_alarmas["clave"]} , {"$set" : {"status" : statusActual}})
                    else:
                        objInsert = {
                            "clave"         :   conf_alarmas["clave"],
                            "nombre_alarma" :   conf_alarmas["nombre_alarma"],
                            "status"        :   statusActual,
                            "texto_largo"   :   conf_alarmas["texto_largo"],
                            "hora_reg"      :   hora_reg,
                            "visto"         :   0
                        }
                        db["notificaciones"].insert_one(objInsert)

        return result

    def enviaTrap(self, alarma, almOid, snmpServidor):
        iterator = sendNotification(
            SnmpEngine(), 
            CommunityData('public', mpModel=0),
            UdpTransportTarget((snmpServidor, 162)),
		    ContextData(),
		    'trap',
		    NotificationType(ObjectIdentity(almOid)).addVarBinds(
                ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),
                ('1.3.6.1.2.1.1.1.0', OctetString(alarma))).loadMibs('SNMPv2-MIB'))

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print(errorIndication)
