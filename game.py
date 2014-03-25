import pygame, sys
from pygame.locals import *

import board

# Constants
TILE_SIZE = 55
LINE_THICKNESS = 1
MARGIN = 20
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
CROSS_COLOR = (0, 0, 255)
NOUGHT_COLOR = (0, 155, 0)
PROGRAM_NAME = 'Mega3T'
FONT = 'courier new'
FONT_SIZE = 16

BOARD_STYLE = {
    'background-color'  :   BACKGROUND_COLOR,
    'small-border-color':   (0, 0, 0),
    'big-border-color'  :   (255, 0, 0),
    'highlight-color'   :   pygame.Color(0, 0, 0, 32),
    'allowed-moves-color':  pygame.Color(0, 255, 0, 32),
    'font-name'         :   FONT,
    'font-size'         :   FONT_SIZE,
    'text-color'        :   TEXT_COLOR
}

# Initialize board instance.
b = board.Board(
        [board.Cross(CROSS_COLOR), board.Nought(NOUGHT_COLOR)],
        TILE_SIZE,
        LINE_THICKNESS,
        MARGIN,
        BOARD_STYLE
    )

# Set up PyGame display.
window_size = (b.get_size() + 160, b.get_size())
pygame.init()
window = pygame.display.set_mode(window_size)
window.fill(BACKGROUND_COLOR)
pygame.display.set_caption(PROGRAM_NAME)

# Render and blit title, and turn.
bold = pygame.font.Font(pygame.font.match_font(FONT, bold=True), 21)
title = bold.render(PROGRAM_NAME, False, TEXT_COLOR)
window.blit(title, (b.get_size(), MARGIN))

font = pygame.font.Font(pygame.font.match_font(FONT), FONT_SIZE)
turn_text = font.render('', False, TEXT_COLOR)
def draw_turn(turn_text, turn_str):
    """Override the turn text to show who's turn it is."""
    # Draw a white rectangle over the old text, then write a new text!
    override_rect = pygame.Rect((b.get_size(), MARGIN+title.get_rect().height), turn_text.get_rect().size)
    pygame.draw.rect(window, BACKGROUND_COLOR, override_rect)
    turn_str = 'Turn: ' + turn_str
    turn_text = font.render(turn_str, False, TEXT_COLOR)
    window.blit(turn_text, (b.get_size(), MARGIN+title.get_rect().height))
    return turn_text

# Initialize board graphics, start game.
b.pygame_init()
window.blit(b.outer_surface, (0, 0))
pygame.display.update()
turn_text = draw_turn(turn_text, b.get_turn_text())

# Main loop
highlight = None
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEMOTION:
            # Give the tile under the cursor a grey highlight.
            pos = b.pos_in_board(event.pos)

            if pos and b.pos_to_coords(pos) in b.allowed_moves:
                # Remove the old highlighted tile and replace it by this one.
                b.del_highlights(highlight, BOARD_STYLE['highlight-color'])
                highlight = b.pos_to_coords(pos)
                b.add_highlight(highlight)

            # Or just remove it if the cursor is outside the board.
            else:
                b.del_highlights(highlight, BOARD_STYLE['highlight-color'])
                highlight = None
            b.draw_highlights()

        elif event.type == MOUSEBUTTONUP:
            # If we're clicking on the board somewhere, make a move.
            pos = b.pos_in_board(event.pos)
            if pos:
                if b.make_a_move(b.pos_to_coords(pos)):
                    turn_text = draw_turn(turn_text, b.get_turn_text())

    window.blit(b.outer_surface, (0, 0))
    pygame.display.update()
