def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    for row in board:
        if all([spot == player for spot in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    for _ in range(9):
        print_board(board)
        row = int(input(f"Player {players[current_player]}, enter row (0-2): "))
        col = int(input(f"Player {players[current_player]}, enter column (0-2): "))

        if board[row][col] == " ":
            board[row][col] = players[current_player]
            if check_winner(board, players[current_player]):
                print_board(board)
                print(f"Player {players[current_player]} wins!")
                return
            current_player = 1 - current_player
        else:
            print("Spot already taken. Try again.")

    print_board(board)
    print("It's a tie!")

tic_tac_toe()
