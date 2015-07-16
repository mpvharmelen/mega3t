# Regular configuration
from constants import *

# This is a function to avoid circular dependency
def get_pieces():
    """The pieces to be used in the game"""
    return pieces.Cross(CROSS_COLOR), pieces.Nought(NOUGHT_COLOR), pieces.Nought(CROSS_COLOR)

# Debugging configuration
import logging
FORCE_MOVE = True
GAME_LOGGING_LEVEL = logging.INFO
BOARD_LOGGING_LEVEL = logging.INFO
PIECES_LOGGING_LEVEL = logging.INFO

# This is at the end of the file to avoid circular dependency
import pieces
