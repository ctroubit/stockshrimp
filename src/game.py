import pygame
from const import *
from board import Board

class Game:
    def __init__(self):
        self.board = Board()

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

                    img = pygame.image.load(piece.texture)
                    img_r = pygame.transform.scale(img,(80,80))
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img_r.get_rect(center=img_center)
                    surface.blit(img_r,piece.texture_rect)


