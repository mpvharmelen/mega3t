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

    def draw(self, surface, pos, size):
        """
        Draw the representation of a piece on the given surface in a square of
        size * size with its top left corner at pos.

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


    def draw(self, surface, pos, size):
        """Draws the representation of a Nought."""
        logger.debug('Nought.draw')
        logger.debug('{}, {}, {}'.format('Surface', surface, type(surface)))
        logger.debug('{}, {}, {}, {}'.format('Pos', pos, type(pos), [type(x) for x in pos]))
        logger.debug('{}, {}, {}'.format('Size', size, type(size)))
        logger.debug('{}, {}, {}'.format('Thickness', self.thickness, type(self.thickness)))

        pos = (int(math.ceil(pos[0] + size/2)), int(math.ceil(pos[1] + size/2)))
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


    def draw(self, surface, pos, size):
        """Draws the representation of a Cross."""
        logger.debug('Cross.draw')
        logger.debug('{}, {}, {}'.format('Surface', surface, type(surface)))
        logger.debug('{}, {}, {}, {}'.format('Pos', pos, type(pos), [type(x) for x in pos]))
        logger.debug('{}, {}, {}'.format('Size', size, type(size)))
        logger.debug('{}, {}, {}'.format('Thickness', self.thickness, type(self.thickness)))

        pygame.draw.line(
            surface,
            self.color,
            (pos[0]+self.margin, pos[1]+self.margin),
            (pos[0]+size-self.margin, pos[1]+size-self.margin),
            self.thickness
        )
        pygame.draw.line(
            surface,
            self.color,
            (pos[0]+size-self.margin, pos[1]+self.margin),
            (pos[0]+self.margin, pos[1]+size-self.margin),
            self.thickness
        )

import random
class RandomAI(AIMixin):
    def __init__(self):
        self.n_rows = None

    def save_board_info(self, n_rows, pieces):
        self.n_rows = n_rows

    def move(self, mutations, allowed_moves):
        return random.choice(allowed_moves)

class NoughtAI(Nought, RandomAI):
    pass

class CrossAI(Cross, RandomAI):
    pass
