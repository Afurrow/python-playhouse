from classes.monster_class import monster, random, attack

class charmander(monster): 
    def __init__(self, level, name='charmander', typ='fire'):
        super().__init__(level, name, typ)
        self._stat_growth = {'hp':3, 'pwr':5, 'dfn':4}
        self._moves = [attack('tackle','normal',30,1,1)
                      ,attack('growl','normal',0,3,1)
                      ,attack('scratch','normal',35,5,0.95)
                      ,attack('ember',self.typ,35,7,0.95)
                      ,attack('headbutt','normal',40,14,0.9)
                      ,attack('fire spin',self.typ,40,16,0.9)
                      ,attack('bodyslam','normal',55,20,0.85)
                      ,attack('flame wheel',self.typ,60,25,0.85)
                      ,attack('rest','normal',0,26,1)
                      ,attack('megaslam','normal',70,33,0.7)
                      ,attack('flamethrower',self.typ,70,34,0.7)
                      ,attack('hyper rush','normal',90,42,0.65)
                      ,attack('fire blast', self.typ,95,49,0.65)]
               
        self.max_hp = int(level * (self._stat_growth['hp']+(random.randint(20,60)/100)) + 2)
        self.max_pwr = int(level * (self._stat_growth['pwr']+(random.randint(20,60)/100)) + 8)
        self.max_dfn = int(level * (self._stat_growth['dfn']+(random.randint(20,60)/100)) + 8)
        self.hp = self.max_hp
        self.pwr = self.max_pwr
        self.dfn = self.max_dfn
        self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]
        
        
class bulbasaur(monster): 
    def __init__(self, level, name='bulbasaur', typ='grass'):
        super().__init__(level, name, typ)
        self._stat_growth = {'hp':5, 'pwr':4, 'dfn':3}
        self._moves = [attack('tackle','normal',30,1,1)
                      ,attack('growl','normal',0,3,1)
                      ,attack('scratch','normal',35,5,0.95)
                      ,attack('vine whip',self.typ,35,7,0.95)
                      ,attack('headbutt','normal',40,14,0.9)
                      ,attack('seed burst',self.typ,40,16,0.9)
                      ,attack('bodyslam','normal',55,20,0.85)
                      ,attack('seed blast',self.typ,60,25,0.85)
                      ,attack('rest','normal',0,26,1)
                      ,attack('megaslam','normal',70,33,0.7)
                      ,attack('giga drain',self.typ,70,34,0.7)
                      ,attack('hyper rush','normal',90,42,0.65)
                      ,attack('tree slam', self.typ,95,49,0.65)]
               
        self.max_hp = int(level * (self._stat_growth['hp']+(random.randint(20,60)/100)) + 2)
        self.max_pwr = int(level * (self._stat_growth['pwr']+(random.randint(20,60)/100)) + 8)
        self.max_dfn = int(level * (self._stat_growth['dfn']+(random.randint(20,60)/100)) + 8)
        self.hp = self.max_hp
        self.pwr = self.max_pwr
        self.dfn = self.max_dfn
        self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]
        

class squirtle(monster): 
    def __init__(self, level, name='squirtle', typ='water'):
        super().__init__(level, name, typ)
        self._stat_growth = {'hp':4, 'pwr':3, 'dfn':5}
        self._moves = [attack('tackle','normal',30,1,1)
                      ,attack('growl','normal',0,3,1)
                      ,attack('scratch','normal',35,5,0.95)
                      ,attack('bubble',self.typ,35,7,0.95)
                      ,attack('headbutt','normal',40,14,0.9)
                      ,attack('water gun',self.typ,40,16,0.9)
                      ,attack('bodyslam','normal',55,20,0.85)
                      ,attack('bubblebeam',self.typ,60,25,0.85)
                      ,attack('rest','normal',0,26,1)
                      ,attack('megaslam','normal',70,33,0.7)
                      ,attack('surf',self.typ,70,34,0.7)
                      ,attack('hyper rush','normal',90,42,0.65)
                      ,attack('hydro blast', self.typ,95,49,0.65)]
               
        self.max_hp = int(self.level * (self._stat_growth['hp']+(random.randint(20,60)/100)) + 2)
        self.max_pwr = int(self.level * (self._stat_growth['pwr']+(random.randint(20,60)/100)) + 8)
        self.max_dfn = int(self.level * (self._stat_growth['dfn']+(random.randint(20,60)/100)) + 8)
        self.hp = self.max_hp
        self.pwr = self.max_pwr
        self.dfn = self.max_dfn
        self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]
        
        
class munchlax(monster): 
    def __init__(self, level, name='munchlax', typ='normal'):
        super().__init__(level, name, typ)
        self._stat_growth = {'hp':5, 'pwr':3, 'dfn':4}
        self._moves = [attack('tackle','normal',30,1,1)
                      ,attack('growl','normal',0,3,1)
                      ,attack('scratch','normal',35,5,0.95)
                      ,attack('headbutt','normal',40,14,0.9)
                      ,attack('bodyslam','normal',55,20,0.85)
                      ,attack('rest','normal',0,26,1)
                      ,attack('megaslam','normal',70,33,0.7)
                      ,attack('hyper rush','normal',90,42,0.65)]
               
        self.max_hp = int(level * (self._stat_growth['hp']+(random.randint(20,60)/100)) + 2)
        self.max_pwr = int(level * (self._stat_growth['pwr']+(random.randint(20,60)/100)) + 8)
        self.max_dfn = int(level * (self._stat_growth['dfn']+(random.randint(20,60)/100)) + 8)
        self.hp = self.max_hp
        self.pwr = self.max_pwr
        self.dfn = self.max_dfn
        self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]
        

class happiny(monster): 
    def __init__(self, level, name='happiny', typ='normal'):
        super().__init__(level, name, typ)
        self._stat_growth = {'hp':5, 'pwr':3, 'dfn':4}
        self._moves = [attack('tackle','normal',30,1,1)
                      ,attack('growl','normal',0,3,1)
                      ,attack('scratch','normal',35,5,0.95)
                      ,attack('headbutt','normal',40,14,0.9)
                      ,attack('bodyslam','normal',55,20,0.85)
                      ,attack('rest','normal',0,26,1)
                      ,attack('megaslam','normal',70,33,0.7)
                      ,attack('hyper rush','normal',90,42,0.65)]
               
        self.max_hp = int(level * (self._stat_growth['hp']+(random.randint(20,60)/100)) + 2)
        self.max_pwr = int(level * (self._stat_growth['pwr']+(random.randint(20,60)/100)) + 8)
        self.max_dfn = int(level * (self._stat_growth['dfn']+(random.randint(20,60)/100)) + 8)
        self.hp = self.max_hp
        self.pwr = self.max_pwr
        self.dfn = self.max_dfn
        self.moves = [m for m in self._moves if m.lvl_lrnd <= self.level]