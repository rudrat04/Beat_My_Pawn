from Board import Board
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
from ChessEngine import evaluate_board, get_best_move
import pygame
import pygame.font

def main():
    board = Board('white')
    winner = None

    pygame.display.init()
    pygame.font.init()
    
    # Set up the display
    win = pygame.display.set_mode((800, 800))  # Adjust to the size of your board
    square_size = 800 // 8

    # Initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont('Helvetica', 100)
 
    # Game loop
    running = True
    selected_piece = None  # Variable to keep track of the currently selected piece
    in_check = False  # Variable to keep track of whether the current player is in check
    valid_moves = []
    
    while running:
        player_moves = board.get_all_player_moves(board.get_current_player_color())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not board.is_game_over:  # Add this condition
                # Get the position of the mouse click
                y, x = pygame.mouse.get_pos()
                # Convert the screen coordinates to board coordinates
                row, col = x // square_size, y // square_size

                # Get the piece at the clicked square
                piece = board.get_piece(row, col)
    
                if selected_piece is None:
                    clicked_piece = piece if piece is not None and piece.color == board.get_current_player_color() else None
                    if clicked_piece is not None:
                        selected_piece = clicked_piece  # Set the selected piece
                        valid_moves = [move for p, move in player_moves if p == selected_piece]
                        board.highlighted_squares = valid_moves
                else:
                    if (row, col) in valid_moves:
                        selected_piece.move((row, col), board)
                        board.highlighted_squares = []
                        board.draw_board(win)
                        selected_piece = None
                    else:
                        clicked_piece = piece if piece is not None and piece.color == board.get_current_player_color() else None
                        if clicked_piece is not None:
                            selected_piece = clicked_piece  # Set the selected piece
                            valid_moves = [move for p, move in player_moves if p == selected_piece]
                            board.highlighted_squares = valid_moves
                        else:
                            selected_piece = None
                            board.highlighted_squares = []

        # Check for game over conditions after the AI move
        if board.check_threefold_repetition():
            print("Draw due to threefold repetition!")
            board.is_game_over = True
        elif not player_moves:
            if board.is_in_check(board.get_current_player_color()):
                board.is_game_over = True
                winner = "White"
                print("Checkmate! White wins!")
            else:
                print("Stalemate! It's a draw!")
                board.is_game_over = True

        # Check if it's the AI player's turn
        # Check if it's the AI player's turn
        if board.get_current_player_color() == 'black' and not board.is_game_over:
            # Make the AI move
            ai_move = get_best_move(board, depth=3)  # Adjust the depth as needed
            if ai_move is None:
            # The AI player has no valid moves
                if board.is_in_check(board.get_current_player_color()):
                    board.is_game_over = True
                    winner = "White"
                    print("Checkmate! White wins!")
                else:
                    print("Stalemate! It's a draw!")
                    board.is_game_over = True
            else:
                piece, move = ai_move
                piece.move(move, board)
                board.highlighted_squares = []

        # Draw the board
        board.draw_board(win)

        # If the game is over, display the winner and update the display
        if board.is_game_over:
            if winner:
                textsurface = myfont.render(f'{winner} wins!', False, (255, 0, 0))
            else:
                textsurface = myfont.render('It\'s a draw!', False, (255, 0, 0))

            # Calculate the center coordinates
            text_rect = textsurface.get_rect(center=(win.get_width()/2, win.get_height()/2))

            win.blit(textsurface, text_rect)
            pygame.display.flip()
            break  # Stop the game loop

    # Wait for a while so the player can see the game result
    pygame.time.wait(5000)

    # Quit Pygame
    pygame.quit()
        

if __name__ == "__main__": 
    main()