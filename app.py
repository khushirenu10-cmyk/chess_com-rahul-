import streamlit as st
import chess
import chess.engine

st.set_page_config(page_title="Chess.com Rahul", page_icon="♟️", layout="centered")

st.title("♟️ Chess.com Rahul")
st.write("Play chess against Stockfish in your browser!")

if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "history" not in st.session_state:
    st.session_state.history = []

st.text(str(st.session_state.board))

user_move = st.text_input("Enter your move (e.g., e2e4):")

if st.button("Play Move"):
    try:
        move = chess.Move.from_uci(user_move.strip())
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.history.append(f"Player: {user_move}")

            try:
                engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")
                result = engine.play(st.session_state.board, chess.engine.Limit(time=0.1))
                st.session_state.board.push(result.move)
                st.session_state.history.append(f"Stockfish: {result.move.uci()}")
                engine.quit()
            except Exception as e:
                st.error(f"Engine error: {e}")
        else:
            st.warning("Illegal move! Try again.")
    except Exception as e:
        st.warning("Invalid input. Use format like e2e4.")

st.subheader("Move History")
for h in st.session_state.history:
    st.write(h)

if st.session_state.board.is_game_over():
    st.success(f"Game Over: {st.session_state.board.result()}")
