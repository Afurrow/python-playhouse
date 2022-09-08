from classes.card_class import card
from random import shuffle


class deck:
    def __init__(self, val_dict):        
        suits = ['Heart', 'Diamond', 'Spade', 'Club']
        nums = list(range(2,11)) + ['Jack', 'Queen', 'King', 'Ace']
        self._deck_lst = [(s, n) for s in suits for n in nums] # [('Heart', 2), ('Diamond', 3)] 
        self._deck = [card(s,n,val_dict) for s,n in self._deck_lst]
        self.card_count = len(self._deck)
        
    def show_cards(self):
        for c in self._deck: 
            print(c) 
            
    def shuffle(self):
        shuffle(self._deck)
        
    def give_card(self): 
        self.card_count -= 1
        return self._deck.pop()
    
    def receive_card(self, new_card):
        if type(new_card) == list: 
            self._deck += new_card 
            self.card_count += len(new_card)
        else:  
            self._deck.append(new_card)
            self.card_count += 1  
            
    def get_deck(self): 
        return self._deck
    