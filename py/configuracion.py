from py.parent import Parent
import subprocess


class Configuracion(Parent):
    def __init__(self):
        self.genericInit()

    def initData(self, formData, config = {"source" : "json", "has_id" : False} ):
        self.genericInit()

        if config["source"] == "form":
            self.ConvertirDeFormASimpleObj(formData, self.dbKeys)
            return
        
        self.dbObject = formData

        if(config["has_id"]):
            self._id = formData["_id"]

    def genericInit(self):
        super().__init__("cinderella25", "configuracion_general")
        self.dbKeys = {
            "inputsConvert" :   ["_id", "frecuencia", "antiguedad", "serverIpAddress", "submask", "gateway"],
            "arrays" :          [""],
            "objects" :         [],
            "inputsInsertDb":   ["frecuencia", "antiguedad", "serverIpAddress", "submask", "gateway"],
            "inputsSelectDb":   ["_id","frecuencia", "antiguedad", "serverIpAddress", "submask", "gateway"],
            "ObjectIds":        ["_id"]
        }
        
    
    def guarda(self):
        self._guardaDatos(self.dbKeys)

    def obtenerColeccion(self, filter1):
        return super()._obtenerColeccionObjSimple(self.dbKeys, filter1)
    
    # siguiente generacion de funciones, favor de no usar las anteriores
    def obtenerDocumento(self, filter1):
        return super()._obtenerDocumentoObjSimple(self.dbKeys, filter1)
    
    def guarda2(self):
        self._guardaDatos2()

    def obtenerColeccion2(self, filter1 = {}):
        return self.collection.find(filter1)
    
    def CambiarConfiguracion(direccion_ip, mascara_subred, gateway):
        comando_ip = f"netsh interface ip set address name='Ethernet' static {direccion_ip} {mascara_subred} {gateway}"
        subprocess.run(comando_ip, shell=True, check=True)
