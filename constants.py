from pygame import Color, K_r, K_q, K_f

# Constants
PROGRAM_NAME = 'Mega3T'
TURN_TEXT = 'Turn: '
GAME_OVER_TEXT = "GAME OVER"

BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
CROSS_COLOR = (0, 0, 255)
NOUGHT_COLOR = (255, 0, 0)

FONT = 'courier new'
FONT_SIZE = 16
TITLE_SIZE = 21
ANTI_ALIAS = False

N_ROWS = 3
SIDE_PANEL_SIZE = 160
TILE_SIZE = 55
LINE_THICKNESS = 1
MARGIN = 20
TPS = 50

BUTTON_MARGIN = 2
BUTTON_POSITION = 2 * MARGIN
RESET_KEY = K_r
RESET_BUTTON_TEXT = "[r]estart"
QUIT_KEY = K_q
QUIT_BUTTON_TEXT = "[q]uit"
FORCE_KEY = K_f

BOARD_STYLE = {
    'background-color'       :  BACKGROUND_COLOR,
    'small-border-color'     :  Color(0, 0, 0),
    'big-border-color'       :  Color(255, 0, 0),
    'highlight-color'        :  Color(0, 0, 0, 32),
    'winning-line-color'     :  Color(0, 0, 0, 150),
    'winning-line-thickness' :  10,
    'winning-highlight-alpha':  100,
    'allowed-moves-color'    :  Color(0, 255, 0, 90),
    'last-move-color'        :  Color(0, 0, 0, 33),
    'font-name'              :  FONT,
    'font-size'              :  FONT_SIZE,
    'text-color'             :  TEXT_COLOR
}
