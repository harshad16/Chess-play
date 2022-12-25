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