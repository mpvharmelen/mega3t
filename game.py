import pygame, sys
from pygame.locals import *

import board

WINDOW_SIZE = (800, 680)
BOARD_SIZE = (640, 640)
MARGIN = 20

def in_board(pos):
    if MARGIN < event.pos[0] < BOARD_SIZE[0]+MARGIN and MARGIN < event.pos[1] < BOARD_SIZE[1]+MARGIN:
        return event.pos[0]-MARGIN, event.pos[1]-MARGIN
    return False

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill((255, 255, 255))
pygame.display.set_caption('Mega3T')

# Render and blit title, and turn.
bold = pygame.font.Font(pygame.font.match_font('courier new', bold=True), 21)
title = bold.render('Mega3T', False, (0, 0, 0))
window.blit(title, (680, 20))

font = pygame.font.Font(pygame.font.match_font('courier new'), 16)
turn_text = font.render('', False, (0, 0, 0))
def draw_turn(turn):
    """Override the turn text to show who's turn it is."""
    # omg a global!? Yeah I'm sorry, I got lazy. TODO!
    global turn_text

    # Draw a white rectangle over the old text, then write a new text!
    override_rect = pygame.Rect((680, 20+title.get_rect().height), turn_text.get_rect().size)
    pygame.draw.rect(window, (255, 255, 255), override_rect)
    turn_str = 'Turn: X' if turn else 'Turn: O'
    turn_text = font.render(turn_str, False, (0, 0, 0))
    window.blit(turn_text, (680, 20+title.get_rect().height))

b = board.Board(
        BOARD_SIZE[0]+MARGIN,
        MARGIN,
        {
         'background': (255, 255, 255),
         'border': (0, 0, 0),
         'big': (255, 0, 0),
         'highlight': pygame.Color(0, 0, 0, 32),
         'circle': (0, 155, 0),
         'cross': (0, 0, 255)
        }
    )
window.blit(b.outer_surface, (0, 0))
pygame.display.update()

turn = board.CROSS
draw_turn(turn)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            pos = in_board(event.pos)
            if pos:
                b.highlight_tile(b.pos_to_coords(pos))
        elif event.type == MOUSEBUTTONUP:
            pos = in_board(event.pos)
            if pos:
                if b.set_tile(b.pos_to_coords(pos), turn):
                    turn = not turn

                    draw_turn(turn)

    window.blit(b.outer_surface, (0, 0))
    pygame.display.update()