from py.parent import Parent

class Formulario(Parent):
    def __init__(self):
        self.genericInit()

    def initData(self, formData, source = "json"):
        self.genericInit()

        if source == "form":
            self.ConvertirDeFormASimpleObj(formData, self.dbKeys)
            return
        
        self.dbObject = formData

    def genericInit(self):
        super().__init__("cinderella25", "formulario")
        self.dbKeys = {
            "inputsConvert" :   ["_id","nombre", "edad"],
            "arrays" :          ["traps"],
            "objects" :         [],
            "inputsInsertDb":   ["nombre", "edad","traps"],
            "inputsSelectDb":   ["_id","nombre", "edad","traps"],
            "ObjectIds":        ["_id"]
        }
        
    
    def guarda(self):
        self._guardaDatos(self.dbKeys)

    def obtenerColeccion(self, filter1):
        return super()._obtenerColeccionObjSimple(self.dbKeys, filter1)