# import classes
import classes.trainer_class as tc
from os import path
from yaml import dump, full_load

# function will request input from the user, ensure it works as needed and returns it
def get_input(typ, mn=None, mx=None):
    if typ == int:
        while True:
            try:
                inpt = int(input())
                if inpt >= mn and inpt <= mx:
                    return inpt
                else:
                    print(f'Please enter a number between {mn} and {mx}')
            except ValueError:
                print('Please enter a valid number')
    elif typ == str: 
        return str(input())            
                       
# Takes user through a text battle where they control their first monster
def battle(player,opponent):
    player_mon = player.party[0]
    
    print(f'{player.name.title()} sends out {player_mon.name}.')
    
    if isinstance(opponent, tc.trainer):
        opp_mon = opponent.party[0]
        print(f'{opponent.name} sends out {opp_mon.name}.')
    else:
        opp_mon = opponent
        print(f'A wild {opp_mon.name} appears!')
        
    while True:
        if player_mon.hp < 0:
            print(f'\n{player_mon.name} fainted.  {opponent.name} wins.')
            break
        
        print(f'\n{player.name}\'s turn.  Which move would you like to use?')
        
        move_dict = {}
        
        for x, move in enumerate(player_mon.moves):
            if move.lvl_lrnd <= player_mon.level:
                move_dict[x+1] = move
                print(f'{x+1}. {move.name}\n  type: {move.typ} | power: {move.pwr} | accuracy: {int(move.acc*100)}%')
                
        player_input = get_input(int, 1, len(move_dict))
        mv_used = move_dict[player_input]
        print(f'{player_mon.name} used {mv_used.name}')
        
        dmg = player_mon.calc_dmg(opp_mon, mv_used)
            
        opp_mon.lose_hp(dmg)        
        print(f'{player_mon.name} dealt {dmg} damage.')
        
        if opp_mon.hp < 0:
            print(f'\n{opp_mon.name} fainted.  {player.name} wins!!!')
            player_mon.gain_exp(opp_mon.level)
            break
        else:
            print(f'\n{opponent.name}\'s turn.')
            opp_mv_lst = [x for x in opp_mon.moves if x.lvl_lrnd <= opp_mon.level]
            mv_used = tc.ml.random.choice(opp_mv_lst)
            dmg = opp_mon.calc_dmg(player_mon, mv_used)
            player_mon.lose_hp(dmg)
            print(f'{opp_mon.name} used {mv_used.name}, it dealt {dmg} damage.')
            
# function will set up trainer, their rival, and comence a battle.  Intended for first play through. 
def new_game(): 
    print('What is your name?')
    p1_name = get_input(str)
    p1 = tc.trainer(p1_name)
    
    rival = tc.trainer('Red')

    # select first mon 
    print('Welcome to the game. Who would you like as your first mon?')
    print('The (1) fire, (2) water, (3) grass, or (4) normal type?')
    typ_select = get_input(int, 1, 4)

    if typ_select == 1:
        p1.get_mon(tc.ml.charmander(5))
        rival.get_mon(tc.ml.squirtle(5))
    elif typ_select == 2:
        p1.get_mon(tc.ml.squirtle(5))
        rival.get_mon(tc.ml.bulbasaur(5))
    elif typ_select == 3:
        p1.get_mon(tc.ml.bulbasaur(5))
        rival.get_mon(tc.ml.charmander(5))
    elif typ_select == 4:
        p1.get_mon(tc.ml.munchlax(5))
        rival.get_mon(tc.ml.happiny(5))

    print(f'Ready for your first fight?  Here comes your rival {rival.name}!\n')

    battle(p1,rival)  
    
    return (p1, rival)

# Play game
print('Would you like to start from (1) last save or (2) beginning?')
save_response = get_input(int, 1, 2)
if save_response == 1:
    if path.isfile('save_state.yaml'): 
        with open('save_state.yaml', 'r') as r: 
            state = full_load(r.read())
        p1 = tc.trainer(state[0]['name'],state[0])
        rival = tc.trainer(state[1]['name'],state[1])
    else: 
        print('No save state found, starting game from the beginning.')
        p1, rival = new_game()
else: 
    p1, rival = new_game()

while True: 
    for mon in p1.party:
        mon.full_heal()
        
    print('\nWhat would you like to do?')
    print('1) Battle wild Mon.  2) Battle other Trainer. 3) Battle Rival. 4) Save and Quit')
    selection = get_input(int, 1, 4)
    if selection == 1: 
        lvl = tc.ml.random.choice([*range(1,p1.party[0].level-2)])
        rand_mon = tc.ml.random.choice([tc.ml.bulbasaur(lvl),tc.ml.charmander(lvl),tc.ml.squirtle(lvl),tc.ml.munchlax(lvl),tc.ml.happiny(lvl)])
        battle(p1, rand_mon)
    elif selection == 2:    
        lvl = tc.ml.random.choice([*range(p1.party[0].level-5,p1.party[0].level+3)])
        rand_trainer = tc.trainer('Eager Trainer')
        rand_mon = tc.ml.random.choice([tc.ml.bulbasaur(lvl),tc.ml.charmander(lvl),tc.ml.squirtle(lvl),tc.ml.munchlax(lvl),tc.ml.happiny(lvl)])
        rand_trainer.get_mon(rand_mon)
        battle(p1, rand_trainer)
    elif selection == 3: 
        lvl = tc.ml.random.choice([*range(p1.party[0].level-3,p1.party[0].level+4)])
        for mon in rival.party: 
            mon.update_lvl(lvl)
        battle(p1, rival)
    else: 
        with open('save_state.yaml','w') as f: 
            f.write(dump([p1.export(), rival.export()],sort_keys=False))
            
        print('Thanks for playing!!!')
        break