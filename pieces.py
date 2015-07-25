import pygame, math, logging
from config import PIECES_LOGGING_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(PIECES_LOGGING_LEVEL)

class AIMixin(object):
    def save_board_info(self, n_rows, pieces):
        """
        Save the info of the board to the AI object, so it can be used for
        the algorithm. Called once, before the first call to move.

        The return value is ignored.
        """
        return NotImplemented

    def move(self, mutations, allowed_moves):
        """
        Make a move

        Must return a (x, y) tuple of the coordinates of the next move.
        (0, 0) is top left,
        (board.n_rows ** 2, board.n_rows ** 2) is bottom right.

        mutations is a list of (piece, (x, y)) tuples of the moves made
        after your last move.

        allowed_moves is a list of coordinates showing you the squares you are
        allowed to play.
        """
        return NotImplemented


class Piece(object):
    def __init__(self, name, abbr, color, thickness=2):
        self.name = name
        self.abbr = abbr
        self.color = color
        self.thickness = thickness

    def __repr__(self):
        return '{}'.format(self.abbr)

    def draw(self, surface):
        """
        Draw the representation of a piece on the given surface (which
        represents a tile).

        The return value is ignored.
        """
        return NotImplemented

    def is_AI(self):
        return isinstance(self, AIMixin)


class Nought(Piece):
    def __init__(self, color):
        name = 'nought'
        abbr = 'O'
        self.size = 0.9
        super(Nought, self).__init__(name, abbr, color)

        logger.debug('Nought.__init__')
        logger.debug('{}, {}'.format(self.thickness, type(self.thickness)))


    def draw(self, surface):
        """Draws the representation of a Nought."""
        logger.debug('Nought.draw')
        logger.debug('{}, {}, {}'.format('Surface', surface, type(surface)))
        logger.debug('{}, {}, {}'.format('Thickness', self.thickness, type(self.thickness)))

        size = max(surface.get_size())
        pos = (int(math.ceil(size/2)), int(math.ceil(size/2)))
        logger.debug('{}, {}, {}'.format('Size', size, type(size)))
        logger.debug('{}, {}, {}, {}'.format('Pos', pos, type(pos), [type(x) for x in pos]))
        pygame.draw.circle(
            surface,
            self.color,
            pos,
            int(size/2*self.size),
            self.thickness
        )


class Cross(Piece):
    def __init__(self, color):
        name = 'cross'
        abbr = 'X'
        self.margin = 4
        super(Cross, self).__init__(name, abbr, color)


    def draw(self, surface):
        """Draws the representation of a Cross."""
        logger.debug('Cross.draw')
        logger.debug('{}, {}, {}'.format('Surface', surface, type(surface)))
        logger.debug('{}, {}, {}'.format('Thickness', self.thickness, type(self.thickness)))

        # logger.debug('{}, {}, {}, {}'.format('Pos', pos, type(pos), [type(x) for x in pos]))
        # logger.debug('{}, {}, {}'.format('Size', size, type(size)))
        pygame.draw.line(
            surface,
            self.color,
            (self.margin, self.margin),
            (surface.get_width()-self.margin, surface.get_height()-self.margin),
            self.thickness
        )
        pygame.draw.line(
            surface,
            self.color,
            (surface.get_width()-self.margin, self.margin),
            (self.margin, surface.get_height()-self.margin),
            self.thickness
        )

import random
class RandomAI(AIMixin):
    def save_board_info(self, n_rows, pieces):
        pass

    def move(self, mutations, allowed_moves):
        return random.choice(allowed_moves)

class NoughtAI(Nought, RandomAI):
    pass

class CrossAI(Cross, RandomAI):
    pass

class CountingAI(AIMixin):
    """
    Representation
    ==============

    Count number of pieces of all players in each megatile. Use the representation
    of the megatile the AI should play in linked to the number of pieces in the
    other megatiles as a key to learn.
    E.g. (this is probably an illegal board)

     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
    X| |X |  |O|  |  |O|
    -+-+- | -+-+- | -+-+-
     |X|  |  |X|  |  |O|
          |       |
    ------+-------+------
          |       |
    X| |  | O|O|X |  | |
    -+-+- | -+-+- | -+-+-
     | |X |  |X|O | O| |
    -+-+- | -+-+- | -+-+-
     | |  | O| |  |  | |
          |       |
    ------+-------+------
          |+-----+|
     | |  || | | ||  | |
    -+-+- ||-+-+-|| -+-+-
     | |  || |O| ||  | |
    -+-+- ||-+-+-|| -+-+-
     | |X ||X| | ||  |O|
           +-----+    ^
              ^       ^ O's last move
              ^ X's next move

    Will be represented something like:
         |     |
         |     |
    3   0|1   1|0   2
    -----+-----+-----
         |     |
         |  O  |
    2   0|2   4|0   1
    -----+-----+-----
         |     |
      X  |     |
    1   0|1   1|0   1


    Learning
    ========

    during the game:
        If a board hasn't been encountered before, each of the nine cells will
            get a certain initial value.
        A weighted random choice is made between the cells
            and is saved to the history of this game (i.e. a board with a choice
            will be saved).

    If the game ends in a victory:
        all choices will be "rewarded" by increasing the value assigned to that
        choice.
    If the game end in a loss:
        all choices will be "punished" by decreasing the value assigned to that
        choice.
    If the game is a draw:
        I have no idea what works best yet.

    """
    ...
