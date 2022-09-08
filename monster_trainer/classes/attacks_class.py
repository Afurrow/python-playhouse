class attack(): 
    def __init__(self, name, typ, pwr, lvl_lrnd, acc):
        self.name = name
        self.typ = typ
        self.pwr = pwr
        self.lvl_lrnd = lvl_lrnd
        self.acc = acc
    
    def export(self): 
        info = {'name':self.name
                ,'typ':self.typ
                ,'pwr':self.pwr
                ,'lvl_lrnd':self.lvl_lrnd
                ,'acc':self.acc
               }
        return info