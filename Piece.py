import pygame

class Piece:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board
        self.hasMoved = False
        # Load the image
        image = pygame.image.load(f"Image/{color}-{self.__class__.__name__}.png")

        # Get the current size
        width, height = image.get_size()

        # Scale the image to 75% of its original size
        self.image = pygame.transform.scale(image, (int(width * 0.75), int(height * 0.75)))

    def get_direction(self):
        return 1 if self.board.turn % 2 == 0 else -1
    
    def draw(self, win):
        x, y = self.position
        win.blit(self.image, (y * 100, x * 100))  # Draw the image at the correct position

    def get_name(self):
        return self.name
    
    def move(self, destination, board, theoretical_move=False):
        
        # Save the current state of the board and piece
        old_state = {
        'position': self.position,
        'destination': destination,
        'piece': self,
        'captured': board.get_piece(destination[0], destination[1]),
        'en_passant_target': board.en_passant_target,
        'hasMoved': self.hasMoved,
        }
        
        board.history.append(old_state)
        if not theoretical_move:
            board.state.append(board.get_state_key())
            board.last_opponent_move = destination

        if isinstance(self, Pawn) and abs(destination[0] - self.position[0]) == 2:
            direction = self.board.black_direction if self.color == 'black' else self.board.white_direction
            if not theoretical_move:
                board.en_passant_target = (self.position[0] - direction, self.position[1])
        elif isinstance(self, Pawn) and destination == board.en_passant_target and not theoretical_move:
            direction = self.board.black_direction if self.color == 'black' else self.board.white_direction
            if destination == board.en_passant_target:
                    board.set_piece(None, destination[0] +  direction, destination[1])
        else:
            board.en_passant_target = None

        if isinstance(self, King):
            if abs(destination[1] - self.position[1]) == 2:
                if not theoretical_move:
                    self.castle(destination)
            self.hasMoved = True

        elif isinstance(self, Rook):
            self.hasMoved = True
        else:
            self.en_passant_target = None
            
      
        # If there's a piece at the destination square
        piece = self.board.get_piece(destination[0], destination[1])
        if piece is not None:
            # And the piece is the opponent's
            if piece.color != self.color:
                # Remove the opponent's piece from the board
                piece = self.board.get_piece(destination[0], destination[1])
                piece = None

        # Save the current state of the board and piece
        old_position = self.position
        old_square = self.board.get_piece(destination[0], destination[1])

        # Move the piece to the destination square
        self.board.set_piece(None, self.position[0], self.position[1])
        board.set_piece(self, destination[0], destination[1])
        self.position = destination
        
        board.turn += 1
        self.hasMoved = True


    def path_is_clear(self, destination):
        dx = 1 if destination[0] > self.position[0] else -1 if destination[0] < self.position[0] else 0
        dy = 1 if destination[1] > self.position[1] else -1 if destination[1] < self.position[1] else 0
        x, y = self.position[0], self.position[1]
        while x != destination[0] or y != destination[1]:
            x += dx
            y += dy
            piece = self.board.get_piece(x,y)
            if x == destination[0] and y == destination[1]:
                break
            if piece is not None:
                return False
        return True

class Pawn(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Pawn'
        self.piece_type = 'P'
    
    # Pawn promotion
    def move(self, destination, board, theoretical_move=False):
        super().move(destination, board, theoretical_move)
        # Check for pawn promotion
        # Check for pawn promotion
        if self.color == 'white' and self.position[0] == self.board.white_promotion_row and not theoretical_move:
            self.promote()
        elif self.color == 'black' and self.position[0] == self.board.black_promotion_row and not theoretical_move:
            self.promote(is_ai=True)

    def promote(self, is_ai=False):
        if is_ai:
            # If the promotion is for the AI, always promote to a queen
            piece_type = 'Q'
        else:
            # If the promotion is for the human player, ask for the piece type
            piece_type = input("Promote pawn to (Q/R/B/N): ")

        # Remove the pawn from the board
        self.board.set_piece(None, self.position[0], self.position[1])

        if piece_type.upper() == 'Q':
            self.board.set_piece(Queen(self.color, self.position, self.board), self.position[0], self.position[1])
        elif piece_type.upper() == 'R':
            self.board.set_piece(Rook(self.color, self.position, self.board), self.position[0], self.position[1])
        elif piece_type.upper() == 'B':
            self.board.set_piece(Bishop(self.color, self.position, self.board), self.position[0], self.position[1])
        elif piece_type.upper() == 'N':
            self.board.set_piece(Knight(self.color, self.position, self.board), self.position[0], self.position[1])

    def get_valid_moves(self, consider_captures=False):
        valid_moves = []
        x , y = self.position
        # Implement the rules for pawn movement
        direction = self.board.white_direction if self.color == 'white' else self.board.black_direction

        # Check if the move is within the board boundaries before getting the piece
        if 0 <= x - direction < 8:
            if self.board.get_piece(x - direction, y) is None and not consider_captures:
                valid_moves.append((x - direction, y))
                if not self.hasMoved and 0 <= x - 2 * direction < 8 and self.board.get_piece(x - 2 * direction, y) is None:
                    valid_moves.append((x - 2 * direction, y))
            if (0 <= y - 1 < 8 and ((self.board.get_piece(x - direction, y - 1) is not None and self.board.get_piece(x - direction, y - 1).color != self.color) or (self.board.en_passant_target == (x - direction, y - 1)))) or consider_captures:
                valid_moves.append((x - direction, y - 1))
            if (0 <= y + 1 < 8 and ((self.board.get_piece(x - direction, y + 1) is not None and self.board.get_piece(x - direction, y + 1).color != self.color) or (self.board.en_passant_target == (x - direction, y + 1)))) or consider_captures:
                valid_moves.append((x - direction, y + 1))

        return valid_moves if valid_moves else []  # Return an empty list if there are no valid moves



class Rook(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Rook'
        self.piece_type = 'R'

    def get_valid_moves(self, consider_captures=False):
        valid_moves = []
        # Define the directions in which the rook can move
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.board.get_piece(new_x, new_y)
                    if piece is None:
                        valid_moves.append((new_x, new_y))
                    elif piece.color == self.color and consider_captures:
                        valid_moves.append((new_x, new_y))
                        break
                    elif piece.color != self.color and not isinstance(piece, King):
                        valid_moves.append((new_x, new_y))
                        break
                    elif piece.color != self.color and isinstance(piece, King):
                        valid_moves.append((new_x, new_y))
                    else:
                        break        
        return valid_moves if valid_moves else []  # Return an empty list if there are no valid moves

class Bishop(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Bishop'
        self.piece_type = 'B'

    # Implement the rules for bishop movements
    def get_valid_moves(self, consider_captures=False):
        valid_moves = []
        # Define the directions in which the bishop can move
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.board.get_piece(new_x, new_y)
                    if piece is None:
                        valid_moves.append((new_x, new_y))
                    elif piece.color == self.color and consider_captures:
                        valid_moves.append((new_x, new_y))
                        break
                    elif piece.color != self.color and not isinstance(piece, King):
                        valid_moves.append((new_x, new_y))
                        break
                    elif piece.color != self.color and isinstance(piece, King):
                        valid_moves.append((new_x, new_y))
                    else:
                        break
        return valid_moves if valid_moves else []  # Return an empty list if there are no valid moves
 

class Knight(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Knight'
        self.piece_type = 'N'

    def get_valid_moves(self, consider_captures=False):
        valid_moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:  # Check if the move is within the board
                piece = self.board.get_piece(x, y)
                if piece is None or piece.color != self.color:  # Check if the square is empty or contains an opponent's piece
                    valid_moves.append((x, y))
                elif piece.color == self.color and consider_captures:
                    valid_moves.append((x, y))
                else:
                    continue

        return valid_moves if valid_moves else []  # Return an empty list if there are no valid moves


class Queen(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'Queen'
        self.piece_type = 'Q'

    def get_valid_moves(self, consider_captures=False):
        valid_moves = []
        # Implement the rules for queen movement
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.position[0] + step * dx
                new_y = self.position[1] + step * dy

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.board.get_piece(new_x, new_y)
                    if piece is None:
                        valid_moves.append((new_x, new_y))
                    elif piece.color == self.color and consider_captures:
                        valid_moves.append((new_x, new_y))
                        break
                    elif piece.color != self.color and not isinstance(piece, King):
                        valid_moves.append((new_x, new_y))
                        break
                    elif piece.color != self.color and isinstance(piece, King):
                        valid_moves.append((new_x, new_y))
                    else:
                        break
        return valid_moves if valid_moves else []  # Return an empty list if there are no valid moves

class King(Piece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board)
        self.name = 'King'
        self.hasMoved = False
        self.piece_type = 'K'
    
    def can_castle(self):
        if self.hasMoved:
            return []

        opponent_moves = self.board.get_all_opponent_moves(self.color)

        # Define the potential castling moves based on the color
        castling_moves = [(self.position[0], 2), (self.position[0], 6)] if self.board.player_color == 'white' else [(self.position[0], 1), (self.position[0], 5)]
        valid_moves = []

        for destination in castling_moves:
            # Get the rook's position based on the destination and color
            rook_position = (self.position[0], 0 if destination[1] in [1, 2] else 7)
            rook = self.board.get_piece(rook_position[0], rook_position[1])

            # Check if the rook is in the correct position and hasn't moved
            if rook is None or rook.name != 'Rook' or rook.color != self.color or rook.hasMoved:
                continue

            # Check if the path is clear and not in opponent's moves
            if not self.path_is_clear(rook_position):
                continue

            # Check if the king's current position and destination are not under attack
            if all((self.position[0], i) not in opponent_moves for i in range(min(self.position[1], destination[1]), max(self.position[1], destination[1]) + 1)):
                valid_moves.append(destination)

        return valid_moves


    def castle(self, destination):
         # Get the rook based on the destination
        rook_position = (self.position[0], 0 if destination[1] in [1, 2] else 7)
        if destination[1] == 2:
            new_rook_position = (self.position[0], 3)
        elif destination[1] == 6:
            new_rook_position = (self.position[0], 5)
        elif destination[1] == 1:
            new_rook_position = (self.position[0], 2)
        else:
            new_rook_position = (self.position[0], 4)

        rook = self.board.get_piece(rook_position[0], rook_position[1])

        # Remove the rook from its original position
        self.board.set_piece(None, rook_position[0], rook_position[1])

        # Set the rook to its new position
        self.board.set_piece(rook, new_rook_position[0], new_rook_position[1])

        # Manually update the rook's position
        rook.position = new_rook_position

        # Remove the king from its original position
        self.board.set_piece(None, self.position[0], self.position[1])

        # Set the king to its new position
        self.board.set_piece(self, destination[0], destination[1])

        # Manually update the king's position
        self.position = destination
        Piece.hasMoved = True

    def get_valid_moves(self):
        valid_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        opponent_moves = self.board.get_all_opponent_moves(self.color)

        for dx, dy in directions:
            new_x, new_y = self.position[0] + dx, self.position[1] + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.board.get_piece(new_x, new_y)
                if (piece is None or (piece.color != self.color and not isinstance(piece, King))) and (new_x, new_y) not in opponent_moves:
                    # Check if the new position is adjacent to the opponent's king
                    is_adjacent_to_opponent_king = any(isinstance(self.board.get_piece(new_x + dx, new_y + dy), King) and self.board.get_piece(new_x + dx, new_y + dy).color != self.color for dx, dy in directions if 0 <= new_x + dx < 8 and 0 <= new_y + dy < 8)
                    if not is_adjacent_to_opponent_king:
                        valid_moves.append((new_x, new_y))
        
        # Add castling moves to the list of valid moves
        valid_moves.extend(self.can_castle())
        
        return valid_moves if valid_moves else []  # Return an empty list if there are no valid moves

