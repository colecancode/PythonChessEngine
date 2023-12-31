# Import Modules & Libraries
import global_vars as G
import display_gui as gui
import ai_algorithms as ai
import pygame, chess, time, sys

# Game Settings
TEST_MODE = False
BLACK_AI = 5
WHITE_AI = -1

# Board Setup
G.BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
#puzzle_fen = 'rn3rk1/1b2qp1n/p5Qp/1pp1B1p1/4P3/1BP5/P1P2PPP/R3K1NR b KQ - 3 18'
G.BOARD.set_board_fen(G.BOARD_FEN)
#G.BOARD.set_fen(puzzle_fen)
gui.draw_board()
from_square = None
outcome = None

# Controlling AI Difficulties
def set_ai_difficulty(move, difficulty):
    if difficulty == 0:
        #   No AI
        move = chess.Move.null()
    elif difficulty == 1:
        #   Random moves
        move = ai.select_random_move()
    elif difficulty == 2:
        #   Calculates moves
        move = ai.select_positional_move()
    elif difficulty >= 3:
        #Looks into future and calculate moves
        move = ai.select_predictive_move(difficulty - 1)
    if difficulty >= 0:
        ai.make_ai_move(move)
    return move

# Pygame Display Loop
while not outcome:
    G.CLOCK.tick(60)
    move = None

    if G.BOARD.turn == chess.WHITE:
        move = set_ai_difficulty(move, WHITE_AI)
    if G.BOARD.turn == chess.BLACK:
        move = set_ai_difficulty(move, BLACK_AI)

    # Check Input Events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Reset Highlight on Any Click
            tile_num = gui.tile_pos_to_num(event.pos)
            gui.draw_board()

            # First Click on New Turn -> Select Square
            if from_square == None:
                from_square = gui.make_selection(tile_num)
            # Selected Square Clicked Again -> Unselect Square
            elif from_square == tile_num:
                gui.draw_board()
                from_square = None
            # Potential Move Clicked -> ...
            elif from_square != None:
                # ...If Valid, Highlight & Move Selected Piece
                for move in G.BOARD.legal_moves:
                    if move.from_square == from_square and move.to_square == tile_num:
                        gui.draw_select_square(move.from_square)
                        gui.draw_select_square(move.to_square)
                        gui.print_san(move)
                        G.BOARD.push(move)
                        from_square = None
                # ...If Invalid, Only Select Square Instead
                if from_square != None:
                    from_square = gui.make_selection(tile_num)

        # Window Close -> End Program
        elif event.type == pygame.QUIT:

            ai.get_board_score()

            pygame.display.quit()
            pygame.quit()
            sys.exit()

    # Draw All Pieces on Screen
    for piece_type in range(1, 7):
        w_piece_tiles = G.BOARD.pieces(piece_type, chess.WHITE)
        for tile_num in w_piece_tiles:
            gui.draw_piece(tile_num, piece_type, chess.WHITE)

        b_piece_tiles = G.BOARD.pieces(piece_type, chess.BLACK)
        for tile_num in b_piece_tiles:
            gui.draw_piece(tile_num, piece_type, chess.BLACK)

    # Check End Game Conditions
    outcome = G.BOARD.outcome()
    if not TEST_MODE and outcome:
        gui.determine_outcome(outcome)

    # Update the Display Screen
    pygame.display.update()

# Wait till Exit after Game Over
while True:
    G.CLOCK.tick(60)
    for event in pygame.event.get():
        # Window Close -> End Program
        if event.type == pygame.QUIT:
            outcome = True
            pygame.display.quit()
            pygame.quit()
            sys.exit()
