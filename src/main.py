# main.py

import pygame
import sys
from square import Square
from const import *
from move import Move
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('stockshrimp')
        self.game = Game()
        
    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        clock = pygame.time.Clock()

        while True:
            # Draw the game state
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # If clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)  # Corrected method name
                            dragger.drag_piece(piece)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

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

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        final_row = dragger.mouseY // SQSIZE
                        final_col = dragger.mouseX // SQSIZE
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(final_row, final_col)
                        move = Move(initial, final, dragger.piece)  # Pass the piece

                        print(f"Attempting to move {dragger.piece} from {initial} to {final}")

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            print('Move executed successfully.')
                            game.next_turn(screen)  # Switch turns after the player move
                        else:
                            print("Invalid move attempted.")

                        dragger.undrag_piece()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main = Main()
    main.mainloop()
