from flask import Flask, request, jsonify, render_template, redirect, copy_current_request_context,escape, Markup
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from py.formulario import Formulario
from py.dbController import dbController
from py.notificacion import Notificacion
from py.conexionPuertoSerial import ConexionTarjeta
from py.tarjeta import Tarjeta
from py.configuracion import Configuracion
from py.conf_alarmas import ConfAlarmas
import serial.tools.list_ports
import time
import threading

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config["secret"] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins = "*")
cont = 0
@app.route("/index")
def index():  
    return render_template("index.html")
@app.route("/formulario")
def formulario():  
    return render_template("formulario.html")
@app.route("/guardar", methods=["POST"])
def guardar():
    obj = Formulario()
    obj.initData(request.json)
    obj.guarda()
    return "Los datos se han guardado correctamente."

# socket ========================================================================================== socket
@app.route("/st/<listener>/<data>")
def st(listener, data):
    socketio.emit(listener, data)
    return data

@app.route("/actualiza_datos")
def actualiza_datos():
    objTarjeta = Tarjeta()
    tarjetasDb = objTarjeta.obtenerColeccion({})

    notificaciones_globales = []
    data_sockets = []

    for tjtDb in tarjetasDb:
        conexionObj = ConexionTarjeta(tjtDb)
        conexionObj.leer_tarjeta()
        info_sensores = conexionObj.validacion_sensores()
        
        data_sockets.append({
            "socket": "socket_tarjeta" + tjtDb["codigo"],
            "tarjeta" : objTarjeta.obtenerDocumento({"codigo" : tjtDb["codigo"]}),
            "info_sensores" : info_sensores,
            "nuevas_notif" : []
        })

    objNotificacion = Notificacion()
    nuevas_notif = objNotificacion.obtenerColeccion({"visto" : 0})
    
    for data in data_sockets:
        data["nuevas_notif"] = nuevas_notif
        socketio.emit(data["socket"], Markup(data))

    return Markup(data_sockets)

# threading ============================================ threading

def RevisionPeriodica():
    while True:
        result = actualiza_datos() 
        objGeneral = Configuracion()
        configGeneral = objGeneral.obtenerDocumento({})
        segundosSleep = (configGeneral["frecuencia"] * 60)
        time.sleep(segundosSleep)

threading.Thread(target=RevisionPeriodica).start()

# tarjeta ========================================================================================== tarjeta
@app.route("/tarjeta/<codigo>")
def tarjeta(codigo):
    puertos = []
    puertos_disponibles = serial.tools.list_ports.comports()
    for puerto in puertos_disponibles:
        puertos.append(puerto.device)
    
    objTarjeta = Tarjeta()
    documento = objTarjeta.obtenerDocumento({"codigo" : codigo})
    
    if documento:
        conexionObj = ConexionTarjeta(documento)
        objNotificacion = Notificacion()
        conexionObj.leer_tarjeta()

        server_data = {
            "tarjeta"       :   objTarjeta.obtenerDocumento({"codigo" : codigo}),
            "puertos"       :   puertos,
            "info_sensores" :   conexionObj.validacion_sensores(),
            "nuevas_notif"  :   objNotificacion.obtenerColeccion({"visto" : False})
            }
        
        return render_template("tarjeta.html", server_data = Markup(server_data))
    else:
        return jsonify({'mensaje': 'Elemento no encontrado'}), 404

@app.route("/guardartarjeta", methods=["POST"])
def guardartarjeta():
    obj = Tarjeta()
    obj.initData(request.json, {"source" : "json", "has_id" : True})
    obj.guarda2()

    return "Los datos se han guardado correctamente."
#lecturas ========================================================================================== lecturas

@app.route("/lectura/<codigo>/<epgLabel>")
def lectura(codigo, epgLabel):
    return obtener_lecturas(codigo, epgLabel, 50)

@app.route("/lectura/<codigo>/<epgLabel>/<limit>")
def todas_lectura(codigo, epgLabel, limit):
    return obtener_lecturas(codigo, epgLabel)

def obtener_lecturas(codigo, epgLabel, limit = False):
    db = dbController("cinderella25").getDb()
    query = {'epgLabel': epgLabel}
    projection = {'valor': 1, 'hora_reg': 1, '_id': 0}

    if limit:
        objs = db["lecturas_" + codigo].find(query, projection).limit(limit).sort('_id', -1)
    else:
        objs = db["lecturas_" + codigo].find(query, projection).sort('_id', -1)

    return jsonify(list(objs))


#Configuracion ========================================================================================== Configuracion
@app.route("/configuracion")
def configuracion():
    objGeneral = Configuracion()
    configGeneral = objGeneral.obtenerDocumento({})
 
    obj = ConfAlarmas()
    alarmas_config = obj.obtenerColeccion({"nombre_alarma": {"$ne": "TBD"}})
    return render_template("configuracion.html", server_data = Markup({"config" : configGeneral, "alarmas_config" : alarmas_config}))

@app.route("/guardarconfiguracidered", methods=["POST"])
def guardarconfiguracidered():
    obj = Configuracion()
    obj.initData(request.json, {"source" : "json", "has_id" : True})
    obj.guarda2()
    # obj.CambiarConfiguracion(obj["serverIpAddress"], obj["submask"], obj["gateway"])
    return "Los datos se han guardado correctamente."

@app.route("/guardarconfiguraciondealarma", methods=["POST"])
def guardarconfiguraciondealarma():
    obj = ConfAlarmas()
    obj.initData(request.json, {"source" : "json", "has_id" : True})
    obj.guarda2()

    return "Los datos se han guardado correctamente."

    

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
    socketio.run(app, host="localhost", port=5000)

    

