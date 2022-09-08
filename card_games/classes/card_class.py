class card: 
    def __init__(self, suit, num, val_dict):
        self._val_dict = val_dict
        self.suit = suit
        self.num = num
        self.val = self._val_dict[num]
        
    def __str__(self):
        return f'{self.num} of {self.suit}s'