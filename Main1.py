from Board import Board
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
import pygame
import pygame.font

def main():
    board = Board('white')
    gameOver = False
    

    # Initialize Pygame
    pygame.init()
 
    # Set up the display
    win = pygame.display.set_mode((800, 800))  # Adjust to the size of your board
    square_size = 800 // 8

    # Initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont('Comic Sans MS', 100)
 
    # Game loop
    running = True
    selected_piece = None  # Variable to keep track of the currently selected piece
    in_check = False  # Variable to keep track of whether the current player is in check
    
    # Initialize player_moves with the valid moves for the starting player
    player_moves = board.get_all_player_moves(board.get_current_player_color())
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameOver:  # Add this condition
                # Get the position of the mouse click
                y, x = pygame.mouse.get_pos()
                # Convert the screen coordinates to board coordinates
                row, col = x // square_size, y // square_size

                # Get the piece at the clicked square
                piece = board.get_piece(row, col)
                clicked_piece = piece if piece is not None and piece.color == board.get_current_player_color() else None
                
                if clicked_piece is not None:
                    selected_piece = clicked_piece  # Set the selected piece
                    player_moves = board.get_piece_valid_moves(selected_piece)
                    board.highlighted_squares = player_moves


                elif (row, col) in board.highlighted_squares and (row, col) in player_moves and selected_piece is not None:

                    selected_piece.move((row, col), board)
                    board.highlighted_squares = []

                     # After a move is made, check for threefold repetition
                    if board.check_threefold_repetition():
                        print("Draw due to threefold repetition!")
                        gameOver = True
                    
                    # Calculate the new possible moves after a move is made
                    player_moves = board.get_all_player_moves(board.get_current_player_color())

                    # If there are no valid moves, check for checkmate or stalemate
                    if not player_moves:
                        if board.is_in_check(board.get_current_player_color()):
                            gameOver = True
                            winner = "White" if board.get_current_player_color() == 'black' else "Black"
                            print(f"Checkmate! {winner} wins!")
                        else:
                            print("Stalemate! It's a draw!")
                            gameOver = True

        # Draw the board
        board.draw_board(win)

        # If the game is over, display the winner and update the display
        if gameOver:
            if winner:
                textsurface = myfont.render(f'{winner} wins!', False, (255, 223, 0))
            else:
                textsurface = myfont.render('It\'s a draw!', False, (255, 223, 0))

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
