import pygame, math, logging
from config import PIECES_LOGGING_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(PIECES_LOGGING_LEVEL)

class AIMixin(object):
    def save_board_info(self, n_rows, pieces):
        """
        Save the info of the board to the AI object, so it can be used for
        the algorithm
        """
        return NotImplemented

    def move(self, mutations):
        """Make a move"""
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
        """Draws the representation of a piece."""
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
