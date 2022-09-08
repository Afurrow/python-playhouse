from random import shuffle


class player:
    def __init__(self, name, cash=2500):
        self._hand = []
        self.cash = cash
        self.name = name
        self.card_count = 0
        
    def show_hand(self):
        for c in self._hand:
            print(c)
    
    def receive_card(self, new_card):
        if type(new_card) == list: 
            self._hand += new_card 
            self.card_count += len(new_card)
        else:  
            self._hand.append(new_card)
            self.card_count += 1        
            
    def discard(self, card):
        self._hand.remove(card)
        self.card_count -= 1
        
    def take_card(self): 
        self.card_count -= 1 
        return self._hand.pop()
    
    def set_hand(self, new_val=[]): 
        self._hand = new_val
        self.card_count = len(self._hand)
        
    def get_hand(self):
        return self._hand
        
    def shuffle_hand(self): 
        shuffle(self._hand)
        
    def hand_len(self): 
        return len(self._hand)
    
    def give_cash(self, val): 
        if self.cash - val < 0: 
            raise ValueError('Insufficient Funds')
        else: 
            self.cash -= val
        return self.cash
    
    def get_cash(self, val=0):
        self.cash += val
        return self.cash