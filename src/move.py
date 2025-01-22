# move.py

class Move:
    def __init__(self, initial, final, piece):
        self.initial = initial  # Square object where the piece is moving from
        self.final = final      # Square object where the piece is moving to
        self.piece = piece      # Piece object being moved

    def __str__(self):
        return f'{self.initial.row},{self.initial.col} -> {self.final.row},{self.final.col}'

    def __repr__(self):
        return f"{self.piece} from {self.initial} to {self.final}"

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (
            self.initial == other.initial and
            self.final == other.final and
            self.piece == other.piece
        )
