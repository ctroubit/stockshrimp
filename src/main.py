import pygame
import sys
from square import Square
from const import *
from move import Move
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('stockshrimp')
        self.game = Game()
        
    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        clock = pygame.time.Clock()

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)
        
            for event in pygame.event.get():

                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX //  SQSIZE
                    
                    # if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece,clicked_row,clicked_col)

                            dragger.save_inital(event.pos)
                            dragger.drag_piece(piece)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # move mouse
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row,motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                    



                # mouse unclicked
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        final_row = dragger.mouseY // SQSIZE
                        final_col = dragger.mouseX // SQSIZE

                        inital = Square(dragger.inital_row,dragger.inital_col)
                        final = Square(final_row,final_col)

                        move = Move(inital,final)

                        if board.valid_move(dragger.piece,move):
                            board.move(dragger.piece,move)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            
                            game.next_turn()


                    dragger.undrag_piece()
                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            clock.tick(60)
            
        
main = Main()
main.mainloop()
 