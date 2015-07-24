# Regular configuration
from constants import *

# Debugging configuration
import logging
FORCE_MOVE = False
GAME_LOGGING_LEVEL = logging.WARN
BOARD_LOGGING_LEVEL = logging.WARN
PIECES_LOGGING_LEVEL = logging.WARN

# This is at the end of the file to avoid circular dependency
import pieces
# This is a function to avoid circular dependency
def get_pieces():
    """The pieces to be used in the game"""
    return pieces.Cross(CROSS_COLOR), pieces.NoughtAI(NOUGHT_COLOR)
