# Tic Tac Toe
def main():
    start_grid = [[' ', ' ',' '],[' ', ' ',' '],[' ', ' ',' ']]
    turn = 1
    game_grid = start_grid
    game_over = False

    while not game_over:
        player = "O" if turn % 2 == 0 else "X"
        display(game_grid, player)
        row, col = check_input(get_input(), game_grid)
        game_grid[row][col] = player
        game_over = check_game_over(game_grid)
        turn += 1

    rematch()

def display(arr, player):
    print()
    print(f'Player "{player}"\'s turn')

    for row in arr:
        print(row)

    print()

def get_input():
    row, col = (0,0)
    while not row in range(1,4):
        row = is_digit(input("Please enter row: "))
    while not col in range(1,4):
        col = is_digit(input("Please enter col: "))
    return (row-1, col-1)

def is_digit(input):
    if input.isdigit():
        return int(input)
    else:
        print("Input must be a digit between 1 and 3")

def check_input(input, game_grid):
    row, col = input
    while game_grid[row][col] != " ":
        print("Cell is already taken please try again")
        row, col = get_input()
    return (row, col)

def check_game_over(game_grid):
    available_spaces = [not " " in row for row in game_grid]
    down_diag = [game_grid[x][x] for x in range(3)]
    up_diag = [game_grid[y][x] for x in range(3)
                               for y in range(2,-1,-1)]

    if all(set(available_spaces)):
        print("Sorry there are no more spaces")
        rematch()

    for row in range(3):
        vert = [game_grid[col][row] for col in range(3)]
        if set(game_grid[row]) == set("X") or set(vert) == set("X") or set(down_diag) == set("X") or set(up_diag) == set("X"):
            print("Congratulations player \"X\" you won!")
            return True
        elif set(game_grid[row]) == set("O") or set(vert) == set("O") or set(down_diag) == set("O") or set(up_diag) == set("O"):
            print("Congratulations player \"O\" you won!")
            return True
    return False

def rematch():
    if input('Type "Play Again" if you would like to play again, anything else to quit ') == "Play Again":
        main()
    else:
        exit()

main()
