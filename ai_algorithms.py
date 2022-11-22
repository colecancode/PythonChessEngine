# Import Modules & Libraries
import math

import chess, pygame, random, time
import display_gui as gui
import global_vars as G

# Select Random Move
def select_random_move():
    legal_moves = list(G.BOARD.legal_moves)
    index = random.randint(0, len(legal_moves) - 1)
    return legal_moves[index]

# Get Game Status

# Get Board Score
def get_board_score():
    if G.BOARD.is_checkmate():
        if G.BOARD.turn:
            return -9999
        else:
            return 9999
    elif G.BOARD.is_stalemate():
        return 0
    elif G.BOARD.is_fivefold_repetition():
        return 0
    elif G.BOARD.is_fifty_moves():
        return 0

    score_data = [G.pawn_score, G.knight_score, G.bishop_score, G.rook_score, G.queen_score, G.king_score]
    black_piece_count = []
    white_piece_count = []
    black_score = 0
    white_score = 0

    for color in [chess.WHITE, chess.BLACK]:
        piece_data = []
        scores = []
        score = 0
        for i in range(1, 7):
            piece_data.append(G.BOARD.pieces(i, color))
        i = 0
        for data in piece_data:
            if color == chess.WHITE:
                white_piece_count.append(len(data))
            else:
                black_piece_count.append(len(data))
            temp = score_data[i]
            temp.reverse()
            scores.append([temp[chess.square_mirror(piece)] for piece in data])
            i+=1
        for arr in scores:
            for num in arr:
                score += num
        if color == chess.WHITE:
            white_score += score
        else:
            black_score += score

    weight = [100, 300, 310, 500, 900]
    material = 0
    n = 0
    for i in white_piece_count:
        if n == 5:
            continue
        material += (i - black_piece_count[n]) * weight[n]
        n+=1
    final = material + white_score - black_score

    if G.BOARD.turn:
        return final
    else:
        return -final


# Select Positional Move
def select_positional_move():
    best_move = (chess.Move.null(), -9999)
    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -get_board_score()
        G.BOARD.pop()
        if score > best_move[1]:
            best_move = (move, score)
    return best_move[0]

# Negamax with Alpha-Beta Pruning
def negamax(depth, alpha, beta):
    # Base Case
    if(depth == 0):
        return get_board_score()
    best_score = -9999
    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -negamax(depth - 1, -beta, -alpha)
        G.BOARD.pop()
        if score > best_score:
            best_score = score

        if score > best_score:
            best_score = score
        if score >= beta:
            return score
        if score > alpha:
            alpha = score
        if alpha >= beta:
            return alpha
    return best_score

# Quiescence Search

# Select Predictive Move
def select_predictive_move(depth):
    alpha = -9999
    beta = 9999

    # Figure out the best move
    best_move = (chess.Move.null(), -9999)

    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -negamax(depth - 1, -beta, -alpha)
        G.BOARD.pop()

        if score > best_move[1]:
            best_move = (move, score)
    return best_move[0]

# Complete AI Move
def make_ai_move(move, delay = 0):
    time.sleep(delay)
    if move != chess.Move.null():
        gui.print_san(move)
        print(get_board_score())
        G.BOARD.push(move)
        gui.draw_board()