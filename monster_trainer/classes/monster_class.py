import random
from classes.attacks_class import attack

class monster(): 
    def __init__(self, level, name, typ, monster_state={}): 
        if len(monster_state)>0:
            self._stat_growth = monster_state['_stat_growth']
            self._moves = [attack(*x.values()) for x in monster_state['_moves']]
            self.level = monster_state['level']
            self.name = monster_state['name']
            self.typ = monster_state['typ']
            self.next_lvl = monster_state['next_lvl']
            self.exp = monster_state['exp']
            self.max_hp = monster_state['max_hp']
            self.max_pwr = monster_state['max_pwr']
            self.max_dfn = monster_state['max_dfn']
            self.hp = monster_state['hp']
            self.pwr = monster_state['pwr']
            self.dfn = monster_state['dfn']
            self.moves = [attack(*x.values()) for x in monster_state['moves']]
        else:
            self.level = level
            self.name = name
            self.typ = typ
            self.next_lvl = self.level*self.level*2
            self.exp = 0  
        
    def calc_dmg(self, opp, mv_used):
        init_dmg = int((((2 * self.level / 5) + 2) * mv_used.pwr * (self.pwr / opp.dfn)) / 20)
        
        if (opp.typ == 'fire' and mv_used.typ == 'water') or (opp.typ == 'water' and mv_used.typ == 'grass') or (opp.typ == 'grass' and mv_used.typ == 'fire'):
            dmg_mltp = 2 
        else: 
            dmg_mltp = 1
            
        init_dmg *= dmg_mltp
        
        return init_dmg
        
    def lose_hp(self, dmg):
        self.hp -= dmg
        
    def level_up(self):
        self.level += 1
        self.next_lvl = self.level*self.level*2
        self.max_hp += random.randint(1,self._stat_growth['hp'])
        self.max_pwr += random.randint(1,self._stat_growth['pwr'])
        self.max_dfn += random.randint(1,self._stat_growth['dfn'])  
        self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]
        self.hp = self.max_hp
        self.pwr = self.max_pwr
        self.dfn = self.max_dfn
    
    def gain_exp(self, opp_lvl):
        exp = (opp_lvl * 8) + (opp_lvl*3*(opp_lvl / self.level))
        self.exp += exp
        print(f'{self.name} gained {int(exp)}.')
        while self.exp >= self.next_lvl:
            self.exp -= self.next_lvl
            self.level_up()
            print(f'Congratulations {self.name} leveled up.  It is now level {self.level}!')
            
    def update_lvl(self, new_lvl):
        if new_lvl < self.level: 
            pass 
        else: 
            self.level = new_lvl
            self.next_lvl = self.level*self.level*2
            self.exp = 0 
            self.max_hp = int(self.level * (self._stat_growth['hp']+(random.randint(20,60)/100)) + 2)
            self.max_pwr = int(self.level * (self._stat_growth['pwr']+(random.randint(20,60)/100)) + 8)
            self.max_dfn = int(self.level * (self._stat_growth['dfn']+(random.randint(20,60)/100)) + 8)
            self.hp = self.max_hp
            self.pwr = self.max_pwr
            self.dfn = self.max_dfn
            self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]        
            
    def export(self): 
        move_dict = []
        move_lst_dict = []
        for m in self._moves:
            move_dict.append(m.export())
        for m in self.moves: 
            move_lst_dict.append(m.export())
            
        info = {'_moves':move_dict 
                 ,'_stat_growth':self._stat_growth
                 ,'name':self.name
                 ,'level':self.level
                 ,'next_lvl':self.next_lvl
                 ,'typ':self.typ
                 ,'max_hp':self.max_hp
                 ,'max_pwr':self.max_pwr
                 ,'max_dfn':self.max_dfn 
                 ,'hp':self.hp 
                 ,'pwr':self.pwr
                 ,'dfn':self.dfn
                 ,'exp':self.exp 
                 ,'moves':move_lst_dict
                }
        return info