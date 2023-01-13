def process_algebraic_notation(algebraic_notation):
    # Process algebraic notation and return a tuple of the form (end, start)
    start = algebraic_notation[:2]
    end = algebraic_notation[2:]
    # Convert the start and end squares to row and column
    start = (int(start[1]) - 1, ord(start[0]) - 97)
    end = (int(end[1]) - 1, ord(end[0]) - 97)

    return end, start


def process_location(algebraic_notation):
    start = algebraic_notation[:2]
    start = (int(start[1]) - 1, ord(start[0]) - 97)
    return start


def convert_to_algebraic_notation(position):
    # Convert a position to algebraic notation
    row, col = position
    return chr(col + 97) + str(row + 1)
