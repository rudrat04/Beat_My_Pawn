from Board import Board
from Piece import Rook, Knight, Bishop, Queen, King, Pawn

def evaluate_board(board):
    score = 0
       # Piece values for material count
    piece_values = {
        Pawn: 100,
        Knight: 320,
        Bishop: 330,
        Rook: 500,
        Queen: 900,
        King: 20000
    }

    pawn_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    knight_table = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    bishop_table = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    rook_table = [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    queen_table = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    king_middle_table = [
        [20, 30, 10, 0, 0, 10, 30, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    king_end_table = [
        [-50, -30, -30, -30, -30, -30, -30, -50],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-50, -40, -30, -20, -20, -30, -40, -50]
    ]

    piece_tables = {
        Pawn: pawn_table,
        Knight: knight_table,
        Bishop: bishop_table,
        Rook: rook_table,
        Queen: queen_table,
        King: king_middle_table  # Use king_middle_table by default
    }

    # Calculate material count
    white_material = sum(piece_values[type(piece)] for row in board.board for piece in row if piece and piece.color == 'white')
    black_material = sum(piece_values[type(piece)] for row in board.board for piece in row if piece and piece.color == 'black')
    score += black_material - white_material


    # Determine if it's the endgame based on the provided criteria
    white_queen_count = sum(1 for row in board.board for piece in row if isinstance(piece, Queen) and piece.color == 'white')
    black_queen_count = sum(1 for row in board.board for piece in row if isinstance(piece, Queen) and piece.color == 'black')
    white_piece_count = sum(1 for row in board.board for piece in row if piece is not None and piece.color == 'white')
    black_piece_count = sum(1 for row in board.board for piece in row if piece is not None and piece.color == 'black')

    is_endgame = (
        (white_queen_count == 0 and black_queen_count == 0) or
        (white_queen_count == 1 and white_piece_count <= 2) or
        (black_queen_count == 1 and black_piece_count <= 2)
    )

    # Switch to king_end_table if it's the endgame
    if is_endgame:
        piece_tables[King] = king_end_table

    # Evaluate piece positions
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece:
                piece_type = type(piece)
                color = piece.color
                table = piece_tables[piece_type]
                score -= table[row][col]  # Subtract the value for black pieces

    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over:
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for piece, move in board.get_all_player_moves(board.get_current_player_color()):
            piece.move(move, board, True)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.undo_move()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for piece, move in board.get_all_player_moves(board.get_current_player_color()):
            piece.move(move, board, True)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.undo_move()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth):
    best_score = float('-inf')
    best_move = None
    original_turn = board.turn  # Store the original turn value
    current_player_color = board.get_current_player_color()  # Store the current player color

    valid_moves = board.get_all_player_moves(current_player_color)
    if not valid_moves:
        return None  # Return None when there are no valid moves

    for piece, move in valid_moves:
        piece.move(move, board, True)
        if not board.is_in_check(current_player_color):
            score = minimax(board, depth - 1, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = (piece, move)
        board.undo_move()
        board.turn = original_turn  # Restore the original turn value

    return best_move