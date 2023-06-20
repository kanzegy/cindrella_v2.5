from py.parent import Parent

class Lectura(Parent):
    def __init__(self, codigo):
        self.genericInit(codigo)

    def initData(self, formData, codigo, config = {"source" : "json", "has_id" : False} ):
        self.genericInit(codigo)

        if config["source"] == "form":
            self.ConvertirDeFormASimpleObj(formData, self.dbKeys)
            return
        
        self.dbObject = formData

        if(config["has_id"]):
            self._id = formData["_id"]

    def genericInit(self, codigo):
        super().__init__("cinderella25", "lecturas_" + codigo)
        self.dbKeys = {
            "inputsConvert" :   ["_id","clave", "valor", "unidad", "hora_reg"],
            "arrays" :          [],
            "objects" :         [],
            "inputsInsertDb":   ["clave", "valor", "unidad", "hora_reg"],
            "inputsSelectDb":   ["_id","clave", "valor", "unidad", "hora_reg"],
            "ObjectIds":        ["_id"]
        }
        
    
    def guarda(self):
        self._guardaDatos(self.dbKeys)

    def obtenerColeccion(self, filter1):
        return super()._obtenerColeccionObjSimple(self.dbKeys, filter1)
    
    #siguiente generacion de funciones, favor de no usar las anteriores (guarda/obtenerColeccion)
    def obtenerDocumento(self, filter1):
        return super()._obtenerDocumentoObjSimple(self.dbKeys, filter1)
    
    def guarda2(self):
        self._guardaDatos2()

    def obtenerColeccion2(self, filter1):
        return self.collection.find(filter1)