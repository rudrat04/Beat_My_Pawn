import pygame as py
import Piece

class Board:
    def __init__(self, player_color):
        self.turn = 0
        self.is_game_over = False
        self.black_direction = 0
        self.white_direction = 0
        self.en_passant_target = None
        self.last_opponent_move = None
        self.history = []
        self.state = []
        self.highlighted_squares = []
        self.player_color = player_color
        self.board = self.setup_board(player_color)
        self.draw_board(py.display.set_mode((800, 800)))
        
        
        
    def setup_board(self, player_color):
        board = [[None] * 8 for _ in range(8)]
        if player_color == 'black':
            self.white_direction = -1
            self.black_direction = 1
            self.white_promotion_row = 7
            self.black_promotion_row = 0
            # Create and place the white pieces
            board[0][0] = Piece.Rook('white', (0, 0), self)
            board[0][1] = Piece.Knight('white', (0, 1), self)
            board[0][2] = Piece.Bishop('white', (0, 2), self)
            board[0][3] = Piece.King('white', (0, 3), self)
            board[0][4] = Piece.Queen('white', (0, 4), self)
            board[0][5] = Piece.Bishop('white', (0, 5), self)
            board[0][6] = Piece.Knight('white', (0, 6), self)
            board[0][7] = Piece.Rook('white', (0, 7), self)
            for i in range(8):
                board[1][i] = Piece.Pawn('white', (1, i), self)
            # Create and place the black pieces
            board[7][0] = Piece.Rook('black', (7, 0), self)
            board[7][1] = Piece.Knight('black', (7, 1), self)
            board[7][2] = Piece.Bishop('black', (7, 2), self)
            board[7][3] = Piece.King('black', (7, 3), self)
            board[7][4] = Piece.Queen('black', (7, 4), self)
            board[7][5] = Piece.Bishop('black', (7, 5), self)
            board[7][6] = Piece.Knight('black', (7, 6), self)
            board[7][7] = Piece.Rook('black', (7, 7), self)
            for i in range(8):
                board[6][i] = Piece.Pawn('black', (6, i), self)
            return board
        else:
            self.white_direction = 1
            self.black_direction = -1
            self.white_promotion_row = 0
            self.black_promotion_row = 7
            # Create and place the white pieces
            board[7][0] = Piece.Rook('white', (7, 0), self)
            board[7][1] = Piece.Knight('white', (7, 1), self)
            board[7][2] = Piece.Bishop('white', (7, 2), self)
            board[7][3] = Piece.Queen('white', (7, 3), self)
            board[7][4] = Piece.King('white', (7, 4), self)
            board[7][5] = Piece.Bishop('white', (7, 5), self)
            board[7][6] = Piece.Knight('white', (7, 6), self)
            board[7][7] = Piece.Rook('white', (7, 7), self)
            for i in range(8):
                board[6][i] = Piece.Pawn('white', (6, i), self)
            # Create and place the black pieces
            board[0][0] = Piece.Rook('black', (0, 0), self)
            board[0][1] = Piece.Knight('black', (0, 1), self)
            board[0][2] = Piece.Bishop('black', (0, 2), self)
            board[0][3] = Piece.Queen('black', (0, 3), self)
            board[0][4] = Piece.King('black', (0, 4), self)
            board[0][5] = Piece.Bishop('black', (0, 5), self)
            board[0][6] = Piece.Knight('black', (0, 6), self)
            board[0][7] = Piece.Rook('black', (0, 7), self)
            for i in range(8):
                board[1][i] = Piece.Pawn('black', (1, i), self)
            return board
            
    def undo_move(self):
        if not self.history:
            return
        last_move = self.history.pop()
        piece = last_move['piece']
        piece.position = last_move['position']
        piece.hasMoved = last_move['hasMoved']
        self.set_piece(piece, *piece.position)
        if last_move['captured']:
            self.set_piece(last_move['captured'], *last_move['destination'])
        else:
            self.set_piece(None, *last_move['destination'])
        self.en_passant_target = last_move['en_passant_target']
        self.turn -= 1
        
    def get_piece(self, row, col):
        piece = self.board[row][col]
        if piece is None:
            return None
        return piece

    def set_piece(self, piece, row, col):
        self.board[row][col] = piece

    def get_all_opponent_moves(self, color):
        opponent_moves = []
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is not None and piece.color != color and not isinstance(piece, Piece.King):
                    valid_moves = piece.get_valid_moves(consider_captures = True)
                    opponent_moves.extend(valid_moves)
        return opponent_moves

    def get_all_player_moves(self, color):
        player_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == color:
                    valid_moves = piece.get_valid_moves()
                    for move in valid_moves:
                        player_moves.append((piece, move))
        return player_moves
    
    def get_piece_valid_moves(self, piece):
        valid_moves = []
        piece_moves = piece.get_valid_moves()
        for move in piece_moves:
            piece.move(move, self, True)
            if not self.is_in_check(piece.color):
                valid_moves.append(move)
            self.undo_move()
        return valid_moves

    def get_current_player_color(self):
        return 'white' if self.turn % 2 == 0 else 'black'

    def get_king(self, color):
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color and isinstance(piece, Piece.King):
                    return piece
                
    def is_in_check(self, color):
        king = self.get_king(color)
        opponent_moves = self.get_all_opponent_moves(color)
        return king.position in opponent_moves
                
    def get_square_color(self, row, col):
        # Check if the square is in the list of highlighted squares
        if (col, row) in self.highlighted_squares:
            return (0, 0, 128)  # Return the highlight color
        elif self.last_opponent_move == (col, row):
            return (166, 0, 255)  # Return the highlight color for opponent's last move
        elif self.is_in_check(self.get_current_player_color()) and self.get_king(self.get_current_player_color()).position == (col, row):
            return (255, 0, 0)
        elif (row + col) % 2 == 0:
            return (255, 255, 255)  # Return the color for light squares
        else:
            return (115, 147, 179)  # Return the color for dark squares
                
    def draw_board(self, win):
        for row in range(8):
            for col in range(8):
                square_color = self.get_square_color(row, col)
                py.draw.rect(win, square_color, (row*100, col*100, 100, 100))
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.draw(win)
        py.display.update()
    
    # Define a function to represent a board state uniquely
    def get_state_key(self):
        """Composes a key for a board state based on piece types and their positions."""
        pieces = []
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is not None:  # Check if the square is not empty
                    pieces.append(f"{piece.piece_type}{i}{j}")  # Append the piece type and its position
        return ''.join(pieces)


    def check_threefold_repetition(self):
        # Check if there are enough moves for potential repetition (at least 3)
        if len(self.state) < 3:
            return False

        # Generate the current state key
        current_state_key = self.get_state_key()
        
        # Check for repetition
        return self.state.count(current_state_key) >= 2
