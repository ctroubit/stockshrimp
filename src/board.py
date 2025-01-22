# board.py

from const import *
from square import Square
from piece import *
from move import Move
from copy import deepcopy

class Board:
    def __init__(self):
        # Initialize an 8x8 board with Square instances
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.last_move = None
        self._create()
        self._add_piece('white')
        self._add_piece('black')

    def move(self, piece, move):
        """
        Executes a move on the board.
        """
        initial = move.initial
        final = move.final

        initial_row, initial_col = initial.row, initial.col
        final_row, final_col = final.row, final.col

        # Move the piece to the final square
        self.squares[initial_row][initial_col].piece = None
        self.squares[final_row][final_col].piece = piece

        # Handle pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # Handle castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if diff < 0 else piece.right_rook
                if rook and rook.moves:
                    self.move(rook, rook.moves[-1])  # Execute rook's move

        # Update piece status
        piece.moved = True
        piece.clear_moves()

        # Update the last move
        self.last_move = move

    def castling(self, initial, final):
        """
        Determines if the move is a castling move.
        """
        return abs(initial.col - final.col) == 2

    def valid_move(self, piece, move):
        """
        Checks if a move is valid for the given piece.
        """
        return move in piece.moves

    def find_king(self, color):
        """
        Finds and returns the Square object where the king of the given color is located.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    return self.squares[row][col]
        return None

    def is_in_check(self, color):
        """
        Determines if the player of the given color is in check.
        """
        king_square = self.find_king(color)
        if not king_square:
            # King not found, which should not happen in a standard game
            return True

        opponent_color = 'white'
        opponent_moves = self.get_all_pseudo_moves(opponent_color)

        for move in opponent_moves:
            if move.final == king_square:
                return True
        return False

    def is_checkmate(self, color):
        """
        Determines if the player of the given color is in checkmate.
        """
        if not self.is_in_check(color):
            return False

        # Generate all legal moves for the player
        legal_moves = self.get_all_valid_moves(color)
        if not legal_moves:
            return True
        return False

    def is_stalemate(self, color):
        """
        Determines if the player of the given color is in stalemate.
        """
        if self.is_in_check(color):
            return False

        # Generate all legal moves for the player
        legal_moves = self.get_all_valid_moves(color)
        if not legal_moves:
            return True
        return False

    def is_game_over(self):
        """
        Determines if the game has ended by checkmate or stalemate.
        """
        # Check for white
        if self.is_checkmate('white'):
            print("Black wins by checkmate!")
            return True
        if self.is_stalemate('white'):
            print("Game is a stalemate!")
            return True

        # Check for black
        if self.is_checkmate('black'):
            print("White wins by checkmate!")
            return True
        if self.is_stalemate('black'):
            print("Game is a stalemate!")
            return True

        return False

    def find_king(self, color):
        """
        Finds and returns the Square object where the king of the given color is located.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    return self.squares[row][col]
        return None

    def get_all_pseudo_moves(self, color):
        """
        Retrieves all possible moves for the given color, without considering checks.
        """
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col)  # Populate piece.moves
                    for move in piece.moves:
                        if self.valid_move(piece, move):
                            moves.append(move)
        return moves

    def get_all_valid_moves(self, color):
        """
        Retrieves all valid moves for the given color, ensuring the king is not in check after the move.
        """
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col)  # Populate piece.moves
                    for move in piece.moves:
                        if self.valid_move(piece, move):
                            # Make a copy of the board to simulate the move
                            board_copy = self.copy()
                            board_copy.move(move.piece, move)
                            if not board_copy.is_in_check(color):
                                moves.append(move)
        return moves

    

    def _create(self):
        """
        Initializes all squares on the board.
        """
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def check_promotion(self, piece, final):
        """
        Promotes a pawn to a queen if it reaches the last rank.
        """
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def copy(self):
        """
        Creates a deep copy of the board.
        """
        return deepcopy(self)

    def _add_piece(self, color):
        """
        Adds all pieces to the board for the given color.
        """
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        
        # Add pawns
        for col in range(COLS):
            self.squares[row_pawn][col].piece = Pawn(color)

        # Add knights
        self.squares[row_other][1].piece = Knight(color)
        self.squares[row_other][6].piece = Knight(color)

        # Add bishops
        self.squares[row_other][2].piece = Bishop(color)
        self.squares[row_other][5].piece = Bishop(color)

        # Add rooks
        self.squares[row_other][0].piece = Rook(color)
        self.squares[row_other][7].piece = Rook(color)

        # Add queen
        self.squares[row_other][3].piece = Queen(color)

        # Add king
        self.squares[row_other][4].piece = King(color)

    def calc_moves(self, piece, row, col):
        """
        Calculates all possible/valid moves for a piece at the given position.
        """
        # Clear existing moves before calculating new ones
        piece.clear_moves()

        def pawn_moves():
            steps = 1 if piece.moved else 2
            direction = piece.dir  # Assuming 'dir' is defined in Pawn class (+1 or -1)

            # Forward moves
            start = row + direction
            end = row + (direction * (1 + steps))

            for move_row in range(start, end, direction):
                if Square.in_range(move_row):
                    target_square = self.squares[move_row][col]
                    if target_square.is_empty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move_obj = Move(initial, final, piece)
                        piece.add_move(move_obj)
                    else:
                        break
                else:
                    break

            # Capture moves
            move_row = row + direction
            for move_col in [col + 1, col - 1]:
                if Square.in_range(move_row, move_col):
                    target_square = self.squares[move_row][move_col]
                    if target_square.has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move_obj = Move(initial, final, piece)
                        piece.add_move(move_obj)



        def straight_moves(incrs):
            """
            Handles moves for Bishops, Rooks, and Queens.
            """
            for incr in incrs:
                move_row, move_col = row, col
                while True:
                    move_row += incr[0]
                    move_col += incr[1]

                    if Square.in_range(move_row, move_col):
                        target_square = self.squares[move_row][move_col]
                        if target_square.is_empty():
                            initial = Square(row, col)
                            final = Square(move_row, move_col)
                            move_obj = Move(initial, final, piece)
                            piece.add_move(move_obj)
                        else:
                            if target_square.has_enemy_piece(piece.color):
                                initial = Square(row, col)
                                final = Square(move_row, move_col)
                                move_obj = Move(initial, final, piece)
                                piece.add_move(move_obj)
                            break
                    else:
                        break

        def king_moves():
            """
            Handles King's moves, including castling.
            """
            adjacent_squares = [
                (row + 1, col),     # Bottom
                (row - 1, col),     # Top
                (row, col + 1),     # Right
                (row, col - 1),     # Left
                (row + 1, col + 1), # Bottom Right
                (row + 1, col - 1), # Bottom Left
                (row - 1, col + 1), # Top Right
                (row - 1, col - 1)  # Top Left
            ]

            for move in adjacent_squares:
                move_row, move_col = move
                if Square.in_range(move_row, move_col):
                    target_square = self.squares[move_row][move_col]
                    if target_square.is_empty_or_has_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move_obj = Move(initial, final, piece)
                        piece.add_move(move_obj)

            # Handle castling
            if not piece.moved:
                # Queen-side castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
                    can_castle = True
                    for c in range(1, 4):
                        if self.squares[row][c].has_piece():
                            can_castle = False
                            break
                    if can_castle:
                        # Ensure squares between king and rook are empty
                        initial = Square(row, col)
                        final = Square(row, 2)
                        move_k = Move(initial, final, piece)

                        initial_rook = Square(row, 0)
                        final_rook = Square(row, 3)
                        move_r = Move(initial_rook, final_rook, left_rook)

                        # Link rooks for castling
                        piece.left_rook = left_rook

                        # Add castling moves
                        left_rook.add_move(move_r)
                        piece.add_move(move_k)

                # King-side castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
                    can_castle = True
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece():
                            can_castle = False
                            break
                    if can_castle:
                        initial = Square(row, col)
                        final = Square(row, 6)
                        move_k = Move(initial, final, piece)

                        initial_rook = Square(row, 7)
                        final_rook = Square(row, 5)
                        move_r = Move(initial_rook, final_rook, right_rook)

                        # Link rooks for castling
                        piece.right_rook = right_rook

                        # Add castling moves
                        right_rook.add_move(move_r)
                        piece.add_move(move_k)

        def knight_moves():
            """
            Handles Knight's moves.
            """
            possible_moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]
            for move in possible_moves:
                move_row, move_col = move
                if Square.in_range(move_row, move_col):
                    target_square = self.squares[move_row][move_col]
                    if target_square.is_empty_or_has_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move_obj = Move(initial, final, piece)
                        piece.add_move(move_obj)

        # Determine the type of the piece and calculate moves accordingly
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straight_moves([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        elif isinstance(piece, Rook):
            straight_moves([(1, 0), (0, 1), (-1, 0), (0, -1)])

        elif isinstance(piece, Queen):
            straight_moves([(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)])

        elif isinstance(piece, King):
            king_moves()
