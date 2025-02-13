import chess
import chess.engine

def get_best_move(board):
    engine = chess.engine.SimpleEngine.popen_uci("/path/to/stockfish")
    result = engine.play(board, chess.engine.Limit(time=2.0))
    engine.quit()
    return result.move

def activate_chess_mode(frame):
    print("entered the chess mode")

    # analyze the frame
    # grab the chess state
    # send the state to engine
    # display the move

    return frame
