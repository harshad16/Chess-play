- For checks we will use this table to check if we need to consider castling:

| K   | O-O | O-O-O | O-O ∨ O-O-O | F   |
|-----|-----|-------|-------------|-----|
| 0   | 0   | 0     | 0           | 1   |
| 0   | 0   | 1     | 1           | 1   |
| 0   | 1   | 0     | 1           | 1   |
| 0   | 1   | 1     | 1           | 1   |
| 1   | 0   | 0     | 0           | 1   |
| 1   | 0   | 1     | 1           | 0   |
| 1   | 1   | 0     | 1           | 0   |
| 1   | 1   | 1     | 1           | 0   |

- which is equivalent to `f = ¬(K ∧ (O-O ∨ O-O-O))`
- Implemented in  Python ```not isinstance(piece, King) or not (castling_rights == "O-O" or castling_rights == "O-O-O")```

## Relative Value of Pieces
- For pawns, we'll be using these tables to determine their relative value:

| Rank | Isolated | Connected | Passed | Passed & Connected |
|------|----------|-----------|--------|--------------------|
| 4    | 1.05     | 1.15      | 1.30   | 1.55               |
| 5    | 1.30     | 1.35      | 1.55   | 2.3                |
| 6    | 2.1      | 1.50      | 1.70   | 3.50               |

| Rank | a & h file | b & g file | c & f file | e & d file |
|------|------------|------------|------------|------------|
| 2    | 0.90       | 0.95       | 1.05       | 1.10       |
| 3    | 0.90       | 0.95       | 1.05       | 1.15       |
| 4    | 0.90       | 0.95       | 1.10       | 1.20       |
| 5    | 0.97       | 0.95       | 1.10       | 1.20       |
| 6    | 1.06       | 1.12       | 1.25       | 1.40       |
