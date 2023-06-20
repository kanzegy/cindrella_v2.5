from py.parent import Parent

class ConfAlarmas(Parent):
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
        super().__init__("cinderella25", "conf_alarmas")
        self.dbKeys = {
            "inputsConvert" : ["_id","nombre_alarma", "usado", "texto_largo", "limite", "logica", "oid_set", "oid_clear", "origen", "clave"],
            "arrays" : [],
            "objects" : [],
            "inputsInsertDb" : ["nombre_alarma", "usado", "texto_largo", "limite", "logica", "oid_set", "oid_clear", "origen", "clave"],
            "inputsSelectDb" : ["_id","nombre_alarma", "usado", "texto_largo", "limite", "logica", "oid_set", "oid_clear", "origen", "clave"],
            "ObjectIds": ["_id"]
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