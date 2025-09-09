import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def check_draw(board):
    return all([cell != ' ' for row in board for cell in row])

def computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    return random.choice(empty_cells)

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    
    while True:
        user_row, user_col = map(int, input("Enter your move (row col): ").split())
        if board[user_row][user_col] != ' ':
            print("Cell is already occupied! Try again.")
            continue
        board[user_row][user_col] = 'X'
        
        if check_win(board, 'X'):
            print_board(board)
            print("You win!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        print("Computer's turn:")
        comp_row, comp_col = computer_move(board)
        board[comp_row][comp_col] = 'O'
        
        if check_win(board, 'O'):
            print_board(board)
            print("Computer wins!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        print_board(board)

play_game()
