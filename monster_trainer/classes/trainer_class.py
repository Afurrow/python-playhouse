import classes.monster_library as ml
from statistics import mean

class trainer():
    def __init__(self,name,trainer_state={}): 
        if len(trainer_state) > 0: 
            self.name = trainer_state['name']
            self.party = [ml.monster(x['level'],x['name'],x['typ'],x) for x in trainer_state['party']]
        else: 
            self.name = name 
            self.party = []   
        
    def get_mon(self, mon):
        self.party.append(mon)
        
    def heal_party(self): 
        for x in self.party:
            x.hp = x.max_hp
            x.pwr = x.max_pwr
            x.dfn = x.max_dfn
        
    def get_avg_lvl(self): 
        return mean([x.level for x in self.party])
        
    def export(self):
        party_dict = []
        for mon in self.party: 
            party_dict.append(mon.export())
            
        info = {'name':self.name
                ,'party':party_dict
               }
        return info
        