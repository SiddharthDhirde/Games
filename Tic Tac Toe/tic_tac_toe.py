from random import randint
import os

def display_board(board):
    '''Display the Tic Tac Toe board.'''
    os.system('clear')  # Clears the terminal screen
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

def player_input():
    '''Prompt the players to choose their markers (X or O).'''
    marker = ''
    while marker != 'X' and marker != 'O':
        marker = input("Player 1, choose 'X' or 'O': ").upper()     
    if marker == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')

def choose_first():
    '''Randomly select which player goes first.'''
    flip = randint(0,1)
    if flip == 0:
        return "Player 1"
    else:
        return "Player 2"

def space_check(board, position):
    '''Check if a space on the board is empty.'''
    return board[position] == ' '

def full_board_check(board):
    '''Check if the entire board is full.'''
    return all(board[i] != ' ' for i in range(1, 10))

def player_choice(board):
    '''Prompt the player to choose a position on the board.'''
    position = 0
    while position not in range(1, 10) or not space_check(board, position):
        try:
            position = int(input("Enter your position (1-9): "))
        except ValueError:
            print("Please enter a number!")
    return position

def place_marker(board, marker, position):
    '''Place the marker (X or O) on the board at the specified position.'''
    board[position] = marker

def win_check(board, marker):
    '''Check if a player has won the game.'''
    winning_combinations = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Columns
        (1, 5, 9), (3, 5, 7)              # Diagonals
    ]
    return any(all(board[pos] == marker for pos in combo) for combo in winning_combinations)

def replay():
    '''Ask if the players want to play again.'''
    choice = input("Play again? Enter Y or N: ").upper()    
    return choice == 'Y'

# Main game loop
print("Welcome to Tic Tac Toe!")

while True:
    # Set up the game
    the_board = [' '] * 10
    player1_marker, player2_marker = player_input()
    turn = choose_first()
    print(turn + " will go first!")
    
    play_game = input("Ready to play? Enter Y or N: ").lower()
    if play_game == 'y':
        game_on = True
    else:
        game_on = False
    
    # Game play loop
    while game_on:
        if turn == 'Player 1':
            display_board(the_board)
            position = player_choice(the_board)
            place_marker(the_board, player1_marker, position)
            if win_check(the_board, player1_marker):
                display_board(the_board)
                print("Player 1 wins!")
                game_on = False
            elif full_board_check(the_board):
                display_board(the_board)
                print("It's a tie!")
                game_on = False
            else:
                turn = "Player 2"
        else:
            display_board(the_board)
            position = player_choice(the_board)
            place_marker(the_board, player2_marker, position)
            if win_check(the_board, player2_marker):
                display_board(the_board)
                print("Player 2 wins!")
                game_on = False
            elif full_board_check(the_board):
                display_board(the_board)
                print("It's a tie!")
                game_on = False
            else:
                turn = "Player 1"
    
    if not replay():
        break

# End of the game
