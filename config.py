# Regular configuration
from constants import *

# Debugging configuration
import logging
FORCE_MOVE = False
GAME_LOGGING_LEVEL = logging.INFO
BOARD_LOGGING_LEVEL = logging.INFO
PIECES_LOGGING_LEVEL = logging.INFO

# This is at the end of the file to avoid circular dependency
# from ai import CrossAI, NoughtAI
# from pieces import Cross, Nought
import pieces
# This is a function to avoid circular dependency
def get_pieces():
    """The pieces to be used in the game"""
    return pieces.Cross(CROSS_COLOR), pieces.NoughtAI(NOUGHT_COLOR)
