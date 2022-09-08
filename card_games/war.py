from classes.deck_class import deck
from classes.player_class import player

# create players, deck, shuffle, and distribute cards. 
def start_game(p1_name, p2_name):    
    
    p1 = player(p1_name)
    p2 = player(p2_name)
    val_dict = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}
    d = deck(val_dict)
    d.shuffle()

    while d.card_count > 0: 
        
        p1.receive_card(d.give_card())
        p2.receive_card(d.give_card())
        
    return (p1, p2)

# make each player play a card and dictate the outcome        
def play_round(p1, p2, card_pool=[]):
    p1_card = p1.take_card()
    p2_card = p2.take_card()
    
    
    print(f'{p1.name} plays {p1_card}')
    print(f'{p2.name} plays {p2_card}')   
    
    if p1_card.val > p2_card.val:
        print(f'{p1.name} Wins!\n')
        if len(card_pool) > 0:
            p1.receive_card(card_pool + [p1_card, p2_card])
        else: 
            p1.receive_card([p1_card, p2_card])
    elif p1_card.val < p2_card.val: 
        print(f'{p2.name} Wins!\n')
        if len(card_pool) > 0:
            p2.receive_card(card_pool + [p1_card, p2_card])
        else: 
            p2.receive_card([p1_card, p2_card])
    else: 
        print('WAR!!!')
        card_pool = card_pool + [p1_card, p2_card, p1.take_card(), p2.take_card()]
        play_round(p1, p2, card_pool)    
        
# Play through the game        
print('Please enter name for player one: ')
p1_name = input()
print('Please enter name for player two: ')
p2_name = input()

game_on = 'Y'
while game_on == 'Y':
    game_over = False
    round_num = 1
    p1, p2 = start_game(p1_name, p2_name)

    while not game_over:
        print(f'Round {round_num} - {p1.name}: {p1.card_count} {p2.name}: {p2.card_count}')
        if round_num % 50 == 0:
            p1.shuffle_hand()
            p2.shuffle_hand()
        
        try: 
            play_round(p1, p2)
        except IndexError: 
            winner = p1.name if p1.card_count > p2.card_count else p2.name
            loser = p1.name if p1.card_count < p2.card_count else p2.name
            print(f'{loser} ran out of cards.\n{winner} won, Congratulations!!!')
            game_over = True
            
        round_num += 1
        if p1.card_count == 0 or p2.card_count == 0: 
            winner = p1.name if p1.card_count > 0 else p2.name
            print(f'{winner} won, Congratulations!!!')
            game_over = True
    
    print(f'Final Score - {p1.name}: {p1.card_count} | {p2.name}: {p2.card_count}')
    game_on = input('Would you like to play again? Y/N\n')
    if game_on == 'Y':
        print()               