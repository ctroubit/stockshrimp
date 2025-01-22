import pygame
from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.hovered_square = None
        self.dragger = Dragger()

    # show methods
    def show_bg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234,235,200) # light green
                else:
                    color = (119,154,88) # dark green

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)
    
    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_r = pygame.transform.scale(img,(80,80))
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img_r.get_rect(center=img_center)
                        surface.blit(img_r,piece.texture_rect)

    def show_moves(self,surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                #color, rect and blit

                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#8C3F3F'

                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)
    
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    
    def show_hover(self,surface):
        if self.hovered_square:
            row = self.hovered_square.row
            col = self.hovered_square.col

            color = '#C86464' if (row + col) % 2 == 0 else '#8C3F3F'

            rect = (col * SQSIZE, row * SQSIZE, SQSIZE,SQSIZE)

            pygame.draw.rect(surface,color,rect,width=3)

    def set_hover(self,row,col):
        self.hovered_square = self.board.squares[row][col]


    def show_last_move(self,surface):
        if self.board.last_move:
            inital = self.board.last_move.inital
            final = self.board.last_move.final

            for pos in [inital,final]:
                color = (244,247,116) if (pos.row + pos.col) % 2 == 0 else (172,195,51)

                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)

    def reset(self):
        self.__init__()


