from classes.deck_class import deck
from classes.player_class import player

# create deck and populate with 6 total decks
def create_deck(): 
    val_dict = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':(1,11)}
    house_deck = deck(val_dict)
    for x in range(1,6): 
        house_deck.receive_card(deck(val_dict).get_deck())
    house_deck.shuffle()
    return house_deck

# creates players, and deck
def setup_game(): 
    # player_name = input('Please enter player\'s name')
    player_name = 'Austin'
    p1 = player(player_name)
    house = player('House', 10000)
    house_deck = create_deck()
    return [p1, house, house_deck]

# prints hand as well as hand totals
def show_hand_w_total(player): 
    print(f'{player.name}\'s hand | Total Value: {get_hand_val(player.get_hand())}')
    player.show_hand()
    print()
    
# get bet as input ensures input is above minimum, suffient input, and sufficient funds for both players.
def take_bets(player, house):
    bet = 0
    while bet == 0:
        try:
            p1_input = int(input('What would you like to bet? $50 minimum.'))
            if p1_input < 50:
                print('Bet needs to be at or above the minimum. ($50)')
                raise Exception('Error') 
            else: 
                p1.give_cash(p1_input)
                house.give_cash(p1_input)
                bet = p1_input
        except ValueError as e: 
            if str(e) == 'Insufficient Funds':
                print('Insufficient Funds, Please decrease bet to something you can afford.') 
            else:
                print('Inefficient input, Please enter an integer 50 or higher.')            
    
    return bet*2

# loop through players hand and total up what value they have in their hand.  Will return highest that isn't a bust in case of Ace. 
def get_hand_val(hand): 
    val1 = 0
    val2 = 0
    for x in hand: 
        if type(x.val) == tuple: 
            val1 += x.val[0]
            val2 += x.val[1]
        else: 
            val1 += x.val
            val2 += x.val
    if val1 > 21 and val2 > 21: 
        return 'Bust!!!'
    elif val2 <= 21: 
        return val2 
    else: 
        return val1
            
# lets player receive card and displays new values
def hit(player): 
    print(f'{player.name} hits.')
    player.receive_card(house_deck.give_card())
    total = get_hand_val(player.get_hand())
    show_hand_w_total(player)
    return total

# let's player hit or stand
def player_action(): 
    player_choice = None
    while 1 == 1: 
        player_choice = input('Would you like to Hit (H) or Stand (S)?')
        if player_choice in ['H', 'S']:
            return player_choice
        else: 
            print('Please enter either "H" or "S" (Hit or Stand).')
        print()
        
# get and create players
p1, house, house_deck = setup_game()
round_num = 1

while True:    
    p1.set_hand([])
    house.set_hand([])
    print(f'Round number: {round_num}\n')
    # recreate deck if less than 65 cards are left
    if house_deck.card_count < 65: 
        create_deck()
        print('Replenishing deck')

    # take bets, minimum of 50. 
    bet = take_bets(p1, house)
    
    p1.receive_card(house_deck.give_card())
    house.receive_card(house_deck.give_card())
    p1.receive_card(house_deck.give_card())
    show_hand_w_total(p1)
    
    show_hand_w_total(house)
    house.receive_card(house_deck.give_card())

    while True: 
        while True:
            p1_total = get_hand_val(p1.get_hand())
            if p1_total == 'Bust!!!': 
                break
            else: 
                action = player_action()
            
                if action == 'H': 
                    hit(p1)
                else: 
                    break   
                    
        if p1_total == 'Bust!!!': 
            print(f'Bust, you lose.  Cash goes to the house.')
            house.get_cash(bet)
            break
        else: 
            print('Dealer\'s Play')
            show_hand_w_total(house)
            while 1 == 1:
                house_total = get_hand_val(house.get_hand())
                if house_total == 'Bust!!!': 
                    break
                elif house_total < 17: 
                    hit(house)
                else: 
                    break
                
        if house_total == 'Bust!!!':
            print(f'House busts.  You Win (${bet})!!!\n')
            p1.get_cash(bet)
            break    
        elif p1_total == house_total:
            print(f'Tie goes to the house (${bet})\n')
            house.get_cash(bet)
            break
        elif p1_total < house_total: 
            print(f'You lose.  Cash goes to the house (${bet})\n')
            house.get_cash(bet)
            break
        else: 
            print(f'You Win!!! You have received ${bet}\n')
            p1.get_cash(bet)
            break    

    if input('Would you like to play again? Y/N') == 'Y': 
        round_num += 1
        print()
    else:
        print('\nThanks for playing!!!')
        break      