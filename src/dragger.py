import pygame
from const import *

class Dragger:
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False

    def update_mouse(self, position):
        self.mouseX, self.mouseY = position
    
    def save_initial(self,position):
        self.initial_row = position[1] // SQSIZE
        self.initial_col = position[0] // SQSIZE

    def drag_piece(self,piece):
        self.piece = piece
        self.dragging = True
    
    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def update_blit(self,surface):
        img = pygame.image.load(self.piece.texture)
        img_r = pygame.transform.scale(img,(120,120))
        img_center = (self.mouseX,self.mouseY)
        self.piece.texture_rect = img_r.get_rect(center=img_center)
        surface.blit(img_r,self.piece.texture_rect)



    