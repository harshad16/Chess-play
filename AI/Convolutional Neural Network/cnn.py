""" On hold due to the lack of time """

# import json
#
# from ChessTest.Board.GameState import GameState, print_board
#
# import numpy as np
# import tensorflow as tf
#
#
# def process_game_state(game_state):
#     pieces = {"wR": 1, "wN": 2, "wB": 3, "wQ": 4, "wK": 5, "wP": 6, "bR": 7, "bN": 8, "bB": 9, "bQ": 10, "bK": 11,
#               "bP": 12}
#     processed_board = []
#     for row in game_state:
#         processed_board.append([])
#         for square in row:
#             if square is not None:
#                 if str(square) in pieces:
#                     processed_board[len(processed_board) - 1].append(pieces[str(square)])
#             else:
#                 processed_board[len(processed_board) - 1].append(0)
#
#     processed_game = {'position': processed_board, 'label': 0}
#     return processed_game
#
#
# def load_dataset():
#     # Load the dataset from a file
#     data = []
#     with open('dataset.json') as f:
#         data = json.load(f)
#
#     # Split the data into positions and labels
#     positions = data['positions']
#     labels = data['labels']
#
#     return np.array(positions[0]), np.array(labels[0])
#
#
# # Preprocess the position data
# def preprocess_position(position):
#     # Convert the position list to a NumPy array
#     position = np.array(position, dtype=np.float32)
#
#     # Normalize the position array
#     position /= 15
#
#     # Add an extra dimension to the position array for the channel
#     position = np.expand_dims(position, axis=-1)
#
#     return position
#
#
#     # process_game_state(game.get_board())
#     # game.initialize_board_from_fen("r2q1rk1/pp1npnbp/2p2pp1/3p4/2PP4/2NBPQBP/PP3PP1/R3K2R w KQ - 1 12")
#
# if __name__ == "__main__":
#     game = GameState()
#     game.initialize_board_from_fen("r4rk1/1pq2pp1/p1n1p1b1/4P3/8/6QR/PPP2PP1/2KR1B2 w - - 3 20")
#
#     process_game_state(game.get_board())
#
#     positions, labels = load_dataset()
#
#     positions = preprocess_position(positions)
#     cnn = tf.keras.models.Sequential()
#
#     cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=(8, 8, 1)))
#
#     cnn.add(tf.keras.layers.MaxPooling2D(pool_size=2))
#
#     cnn.add(tf.keras.layers.Flatten())
#
#     cnn.add(tf.keras.layers.Dense(units=64, activation='relu'))
#
#     cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))
#
#     cnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # cnn.fit(x=positions, y=labels, batch_size=32, epochs=10)