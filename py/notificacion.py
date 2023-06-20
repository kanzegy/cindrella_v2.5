from py.parent import Parent

class Notificacion(Parent):
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
        super().__init__("cinderella25", "notificaciones")
        self.dbKeys = {
            "inputsConvert" :   ["_id","clave", "nombre_alarma", "status", "texto_largo", "hora_reg", "visto"],
            "arrays" :          [],
            "objects" :         [],
            "inputsInsertDb":   ["clave", "nombre_alarma", "status", "texto_largo", "hora_reg", "visto"],
            "inputsSelectDb":   ["_id","clave", "nombre_alarma", "status", "texto_largo", "hora_reg", "visto"],
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

    def obtenerColeccion2(self, filter1):
        return self.collection.find(filter1)