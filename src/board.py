from const import *
from square import Square
from piece import *
from move import Move



class Board:
    def __init__(self):
       self.squares = [[0,0,0,0,0,0,0,0]for col in range(COLS)]

    
       self._create()
       self._add_piece('white')
       self._add_piece('black')


    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] =  Square(row,col)
        

    def _add_piece(self, color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)
        for col in range(COLS):
            self.squares[row_pawn][col] =  Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other,2,Bishop(color))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other,3,Queen(color))

        self.squares[5][0] = Square(5,0, King(color))

        # king
        self.squares[row_other][4] = Square(row_other,4,King(color))

    def calc_moves(self,piece,row,col):
        # Calculate all possible/valid moves for a piece in a position

        def pawn_moves():
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for move_row in range(start,end,piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        inital = Square(row,col)
                        final = Square(move_row,col)

                        move = Move(inital,final)

                        piece.add_move(move)

                    else:
                        break

                else:
                    break
        
            move_row = row + piece.dir
            move_cols = [col+1,col-1]

            for move_col in move_cols:
                if Square.in_range(move_row,move_col):
                    if self.squares[move_row][move_col].has_enemy_piece(piece.color):
                        inital = Square(row,col)
                        final = Square(move_row,move_col)

                        move = Move(inital,final)

                        piece.add_move(move)

        def straight_moves(incrs):
            for incr in incrs:
                move_row, move_col = row, col
                while True:
                    move_row += incr[0]
                    move_col += incr[1]

                    if Square.in_range(move_row,move_col):
                        if self.squares[move_row][move_col].is_empty():
                            inital = Square(row,col)
                            final = Square(move_row,move_col)

                            move = Move(inital,final)

                            piece.add_move(move)

                        else:
                            if self.squares[move_row][move_col].has_enemy_piece(piece.color):
                                inital = Square(row,col)
                                final = Square(move_row,move_col)

                                move = Move(inital,final)

                                piece.add_move(move)
                            break
                    else:
                        break

        def king_moves():
            adjacent_squares = [
                (row+1,col), #bottom
                (row-1,col), #top
                (row,col+1), #right
                (row,col-1), #left
                (row+1,col+1), #bottom right
                (row+1,col-1), #bottom left
                (row-1,col+1), #top right
                (row-1,col-1) # top left

            ]
            for move in adjacent_squares:
                move_row, move_col = move
                if Square.in_range(move_row,move_col):
                    if self.squares[move_row][move_col].is_empty_or_has_enemy(piece.color):
                        inital = Square(row,col)
                        final = Square(move_row,move_col)

                        move = Move(inital,final)

                        piece.add_move(move)

            

        def knight_moves():
            possible_moves =[
                (row+2,col+1),
                (row+2,col-1),
                (row-2,col+1),
                (row-2,col-1),
                (row+1,col+2),
                (row+1,col-2),
                (row-1,col+2),
                (row-1,col-2)
            ]
            for move in possible_moves:
                possible_move_row, possible_move_col = move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_has_enemy(piece.color):
                        inital = Square(row,col)
                        final = Square(possible_move_row,possible_move_col)

                        move = Move(inital,final)

                        piece.add_move(move)

        if isinstance(piece,Pawn):
            pawn_moves()

        elif isinstance(piece,Knight):
            knight_moves()

        elif isinstance(piece,Bishop):
            straight_moves([(1,1),(1,-1),(-1,1),(-1,-1)])        
        elif isinstance(piece,Rook):
            straight_moves([(1,0),(0,1),(-1,0),(0,-1)])
        elif isinstance(piece,Queen):   
            straight_moves([(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)])
        elif isinstance(piece,King):
            king_moves()


            

    

    
        

