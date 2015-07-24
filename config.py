from constants import CROSS_COLOR, NOUGHT_COLOR

########################### Debugging configuration ############################
# Set this to True to enable forcing moves. If FORCE_MOVE then the possibility
# of forcing moves can be toggled by pressing constants.FORCE_KEY
FORCE_MOVE = False

import logging
GAME_LOGGING_LEVEL = logging.WARN
BOARD_LOGGING_LEVEL = logging.WARN
PIECES_LOGGING_LEVEL = logging.WARN



############################## Game configuration ##############################
# This is at the end of the file to avoid circular dependency
import pieces
# This is a function to avoid circular dependency
def get_pieces():
    """The pieces to be used in the game"""
    return pieces.Cross(CROSS_COLOR), pieces.NoughtAI(NOUGHT_COLOR)
