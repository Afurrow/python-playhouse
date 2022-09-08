#! python3

from random import shuffle

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6,
          "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10,
          "Queen": 10, "King": 10, "Ace": 11}

class Deck:

    def __init__(self):
        self.all_cards = [Card(s, r) for s in suits
                                     for r in ranks]
        shuffle(self.all_cards)
        
    def deal_one(self):
        return self.all_cards.pop()

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Player:

    def __init__(self, name, chips=10000):
        self.name = name
        self.chips = chips
        self.all_cards = []
        self.score = 0

    def __str__(self):
        return f"{self.name} has {len(self.all_cards)} cards"

    def __len__(self):
        return len(self.all_cards)

    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

        total = 0
        sum_values = sum([x.value for x in self.all_cards])
        for card in self.all_cards:
            if card.rank == 'Ace' and sum_values > 21:
                total += 1
            else:
                total += card.value
        self.score = total

    def gain_chips(self, change):
        self.chips += change

    def lose_chips(self, change):
        self.chips -= change
    
    def clear_hand(self):
        self.all_cards = []

def take_bet(max_bet):
    while True:
        bet = input("Place your bets: ")
        try:
            bet = int(bet)
            if 0 < bet <= max_bet:
                return bet
            else:
                print('Bet must be greater than 0 and less than total chips')
        except:
            print('Bet must be an integer')

def display(house, player):
    print('\n'*10)
    print(f'{house.name} | Hand: {house.score}')
    [print(x) for x in house.all_cards]
    print()   
    [print(x) for x in player.all_cards]
    print(f'{player.name} | Chips: {player.chips} | Hand: {player.score}')

# Setup Players and Deck
deck = Deck()
house = Player("House")
player = Player("Austin") # input("Please enter your name: "))
game_on = True

# Start Round
while game_on:
    bet = take_bet(player.chips)
    house.clear_hand()
    player.clear_hand()
    house.add_cards(deck.deal_one())
    player.add_cards([deck.deal_one(), deck.deal_one()])
    display(house, player)
    house_bust = False
    player_bust = False

    # Player Phase
    while True:
        if player.score > 21:
            print('You Busted!')
            player_bust = True
            break

        else: 
            user_input = input('Would you like to Hit or Stand? ')

            if user_input.lower() == 'hit':
                player.add_cards(deck.deal_one())
                display(house, player)
            elif user_input.lower() == 'stand':
                break

    # House Phase
    if player_bust:
        pass
    else: 
        while house.score < 17:
            house.add_cards(deck.deal_one())
            display(house, player)
            if house.score > 21:
                print('House Busted!')
                house_bust = True
                break

    # Results
    if player_bust or (player.score <= house.score and not house_bust):
        print(f'Sorry, You lost {bet} chips.')
        player.lose_chips(bet)
    elif house_bust or (player.score > house.score and not player_bust):
        print(f"Congratulations! you won {bet} chips!")
        player.gain_chips(bet)

    # Play Again?
    user_input = input("Would you like to play again? (y / n) ")
    if user_input.lower() == 'n':
        game_on = False
