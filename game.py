import sys, logging, pygame

import config
from board import PygameBoard as Board
from constants import *

logging.basicConfig(level=config.GAME_LOGGING_LEVEL)
logger = logging.getLogger(__name__)



def setup_display(program_name):
    """Set up PyGame display."""
    pygame.init()
    pygame.display.set_caption(program_name)

def setup_window(board_size, side_panel_size, background_color):
    """Create window."""
    window_size = (board_size + side_panel_size, board_size)
    window = pygame.display.set_mode(window_size)
    window.fill(background_color)
    return window

def draw_title(window, font, text, position, color=TEXT_COLOR,
               anti_alias=ANTI_ALIAS):
    """Render and blit title."""
    title = font.render(text, anti_alias, color)
    window.blit(title, position)
    return title.get_rect()


def draw_button(window, font, text, position, line_thickness=LINE_THICKNESS,
                color=TEXT_COLOR, anti_alias=ANTI_ALIAS):
    """Draw and return a rectangle with text in it."""
    surface = font.render(text, anti_alias, color)
    rect = surface.get_rect()
    pygame.draw.rect(surface, color, rect, line_thickness)
    window.blit(surface, position)
    rect.topleft = position
    return rect

def draw_turn(window, font, text,
              pos=None, rect=None,
              bg_color=BACKGROUND_COLOR, text_color=TEXT_COLOR,
              anti_alias=ANTI_ALIAS, info_text=TURN_TEXT):
    """Override the turn text to show who's turn it is."""
    if rect:
        # Remove old text
        window.fill(bg_color, rect)
        pos = pos or rect.topleft
        logger.debug('Old surface blanked.')

    # Write new text
    logger.debug('Turn text: ' + text)
    turn_str = info_text + text
    new_surface = font.render(turn_str, anti_alias, text_color)
    window.blit(new_surface, pos)
    return new_surface.get_rect(topleft=pos)

def draw_game_over(window, font, text, pos, text_color=TEXT_COLOR,
                   anti_alias=ANTI_ALIAS):
    """Draw game over text."""
    surface = font.render(text, anti_alias, text_color)
    window.blit(surface, pos)
    return surface.get_rect(topleft=pos)

def remove_game_over(window, rect, bg_color=BACKGROUND_COLOR):
    """Remove game over text."""
    window.fill(bg_color, rect)

def reset(window, font, board, turn_rect, game_over_rect):
    """Reset board and draw turn text."""
    logger.info('Reset')
    board.reset()
    turn_rect = draw_turn(window, font, board.get_turn_text(), rect=turn_rect)
    board.draw_highlights()
    if game_over_rect is not None:
        remove_game_over(window, game_over_rect)
    return turn_rect

def update_display(window, board, position=(0,0)):
    """Update display with boad state."""
    window.blit(board.outer_surface, position)
    pygame.display.update()

def exit():
    """Exit program."""
    logger.info('Exit')
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # Initialize Pygame
    setup_display(PROGRAM_NAME)

    # Initialize board instance.
    b = Board(
            config.get_pieces(),
            TILE_SIZE,
            LINE_THICKNESS,
            MARGIN,
            BOARD_STYLE,
            N_ROWS
        )

    # We're assuming the board is square, so board_size is just an int.
    board_size = b.get_size()

    # Initialize window
    window = setup_window(board_size, SIDE_PANEL_SIZE, BACKGROUND_COLOR)

    # Draw title
    title_font = pygame.font.Font(pygame.font.match_font(FONT, bold=True), TITLE_SIZE)
    title_pos = (board_size, MARGIN)
    title_rect = draw_title(window, title_font, PROGRAM_NAME, title_pos)
    del title_pos

    # Draw reset button
    font = pygame.font.Font(pygame.font.match_font(FONT), FONT_SIZE)
    button_y_pos = board_size - BUTTON_POSITION
    reset_pos = (board_size, button_y_pos)
    reset_rect = draw_button(window, font, RESET_BUTTON_TEXT, reset_pos)
    del reset_pos

    # Draw quit button
    quit_pos = (board_size + reset_rect.width + BUTTON_MARGIN, button_y_pos)
    quit_rect = draw_button(window, font, QUIT_BUTTON_TEXT, quit_pos)
    del quit_pos, button_y_pos

    # Draw turn text
    turn_pos = (board_size, MARGIN + title_rect.height)
    turn_rect = draw_turn(window, font, b.get_turn_text(), turn_pos)
    del turn_pos

    # Initialize game over text
    game_over_pos = MARGIN * 2 + title_rect.height + turn_rect.height
    game_over_pos = (board_size, game_over_pos)
    game_over_rect = None

    # Initialize board graphics
    b.pygame_init()
    update_display(window, b)

    # Initialize main loop
    quit = False
    force_move = config.FORCE_MOVE
    clock = pygame.time.Clock()

    # Main loop
    while not quit:
        # If it's an AI's turn, let it move
        if b.get_turn().is_AI() and not b.game_over:
            ai = b.get_turn()
            if b.make_a_move(ai.move(b.get_mutations(ai), b.allowed_moves)):
                turn_rect = draw_turn(window, font,
                                      b.get_turn_text(), rect=turn_rect)
            else:
                logger.warn("{} made an illegal move".format(ai))


        for event in pygame.event.get():
            if event.type == pygame.QUIT\
               or \
              (event.type == pygame.MOUSEBUTTONUP and
               quit_rect.collidepoint(event.pos))\
               or \
              (event.type == pygame.KEYUP and
               event.key == QUIT_KEY):
                quit = True
                break

            elif event.type == pygame.MOUSEMOTION:
                if not b.game_over:
                    # Give the tile under the cursor a highlight.
                    # First remove the old highlighted tile
                    b.del_highlights(color=BOARD_STYLE['highlight-color'])

                    # Add new highlight
                    pos = b.pos_in_board(event.pos)
                    if pos:
                        coords = b.pos_to_coords(pos)
                        if coords in b.allowed_moves:
                            b.add_highlight(coords)

                    # Draw new highlights
                    b.draw_highlights()

            elif (event.type == pygame.MOUSEBUTTONUP and
                  reset_rect.collidepoint(event.pos))\
                 or \
                 (event.type == pygame.KEYUP and
                  event.key == RESET_KEY):
                    turn_rect = reset(window, font, b, turn_rect, game_over_rect)
                    game_over_rect = None

            elif event.type == pygame.MOUSEBUTTONUP and not b.game_over:
                # If we're clicking on the board somewhere, make a move.
                pos = b.pos_in_board(event.pos)
                if pos:
                    if b.make_a_move(b.pos_to_coords(pos), force_move):
                        turn_rect = draw_turn(window, font,
                                              b.get_turn_text(), rect=turn_rect)

            elif event.type == pygame.KEYUP:
                if config.FORCE_MOVE and event.key == FORCE_KEY:
                    force_move = not force_move
                    logger.info("Force move: {}".format(force_move))


        if b.game_over:
            b.del_highlights(color=b.style['allowed-moves-color'])
            b.draw_highlights()

            game_over_rect = draw_game_over(window, title_font,
                                            GAME_OVER_TEXT, game_over_pos)

        update_display(window, b)
        clock.tick(TPS)

    exit()
