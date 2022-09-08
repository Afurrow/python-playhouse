#! python3

from random import shuffle

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6,
          "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 11,
          "Queen": 12, "King": 13, "Ace": 14}

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:

    def __init__(self):
        self.all_cards = [Card(s, r) for s in suits
                                     for r in ranks]

    def shuffle(self):
        shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Player:

    def __init__(self, name):
        self.name = name
        self.all_cards = []

    def __str__(self):
        return f"{self.name} has {len(self.all_cards)} cards"

    def __len__(self):
        return len(self.all_cards)

    def remove_one(self):
        return self.all_cards.pop(0)

    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

player_1 = Player(input("Player 1 - Please enter your name: "))
player_2 = Player(input("Player 2 - Please enter your name: "))

start_deck = Deck()
start_deck.shuffle()

for i in range(26):
    player_1.add_cards(start_deck.deal_one())
    player_2.add_cards(start_deck.deal_one())

game_on = True
round_num = 0

while game_on:
    round_num += 1
    print(f"Round {round_num}\n"
          f"{player_1.name} card count: {len(player_1)}"
          f"\n{player_2.name} card count: {len(player_2)}")

    if len(player_1.all_cards) == 0:
        print(f"{player_1.name} is out of cards, {player_2.name} wins!")
        game_on = False
        break

    if len(player_2.all_cards) == 0:
        print(f"{player_2.name} is out of cards, {player_1.name} wins!")
        game_on = False
        break

    p1_in_play = []
    p1_in_play.append(player_1.remove_one())
    p2_in_play = []
    p2_in_play.append(player_2.remove_one())

    at_war = True

    while at_war:
        if p1_in_play[-1].value > p2_in_play[-1].value:
            player_1.add_cards(p1_in_play)
            player_1.add_cards(p2_in_play)

            at_war = False

        elif p1_in_play[-1].value < p2_in_play[-1].value:
            player_2.add_cards(p1_in_play)
            player_2.add_cards(p2_in_play)

            at_war = False

        else:
            print("War!")

            if len(player_1.all_cards) < 3:
                print(f"{player_1.name} does not have enough cards to declare war")
                print(f"{player_2.name} wins!")
                game_on = False
                break

            elif len(player_2.all_cards) < 3:
                print(f"{player_2.name} does not have enough cards to declare war")
                print(f"{player_1.name} wins!")
                game_on = False
                break

            else:
                for num in range(3):
                    p1_in_play.append(player_1.remove_one())
                    p2_in_play.append(player_2.remove_one())