import math
import pygame
from pygame.locals import *

CIRCLE = 0
CROSS = 1

class Piece(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def draw(self, coords, size):
        '''Draws the representation of a piece.'''
        raise NotImplemented('You must write this for each piece.')

class Nought(Piece):
    def __init__(self):
        name = 'nought'
        color = (0, 155, 0)
        super(Nought, self).__init__(name, color)

    def draw(self, surface, coords, size):
        pygame.draw.circle(
            surface,
            self.color,
            coords,
            size,
            2 # What the ** is this 2 for?
        )

class Cross(Piece):
    def __init__(self):
        name = 'cross'
        color = (0, 0, 255)
        super(Nought, self).__init__(name, color)

    def draw(self, coords, size):
        ...


class Board(object):
    def __init__(self, pieces, pixl_size, pixl_margin, colors, font='courier new', nr_rows=3):
        self.pieces = []
        for piece in pieces:
            if isinstance(piece, Piece):
                self.pieces.append(piece)
            else:
                raise TypeError('All pieces must be an instance of '
                                '(a subclass of) Piece.')
        self.turn = 0

        self.real_size, self.margin = pixl_size, pixl_margin
        self.size, self.tile_size = pixl_size-pixl_margin, (pixl_size-pixl_margin)/nr_rows**2
        self.colors = colors
        self.nr_rows = nr_rows

        self.tiles = [[None]*nr_rows**2 for i in range(nr_rows**2)]

        self.outer_surface = pygame.Surface((self.real_size, self.real_size))
        self.outer_surface.fill(colors['background'])

        # Draw the row and column numbers.
        font = pygame.font.Font(pygame.font.match_font(font), 16)
        for i in range(nr_rows**2):
            f = font.render(str(i), False, self.colors['border'])
            rect = f.get_rect()
            rect.topleft = (
                self.tile_size*(i+1)-rect.width/2-self.tile_size/2+self.margin,
                self.margin/2-rect.height/2
            )
            self.outer_surface.blit(f, rect)
            rect.topleft = (
                self.margin/2-rect.width/2,
                self.tile_size*(i+1)-rect.height/2-self.tile_size/2+self.margin
            )
            self.outer_surface.blit(f, rect)

        self.surface = pygame.Surface((self.size, self.size))
        self.draw_board()

    def switch_turns(self):
        self.turn = (self.turn + 1) % len(self.pieces)

    def draw_board(self):
        """Draw the board to the surface, with everything on it."""
        self.surface.fill(self.colors['background'])
        for x in range(self.nr_rows**2):
            for y in range(self.nr_rows**2):
                # First draw the tile itself, which is just some borders.
                pos = self.coords_to_pos((x, y))
                rect = pygame.Rect(pos, [self.tile_size]*2)
                pygame.draw.rect(self.surface, self.colors['border'], rect, 1)

                # Then draw a circle or cross in it, if necessary.
                tile = self.tiles[x][y]
                if tile == CIRCLE:
                    pygame.draw.circle(
                        self.surface,
                        self.colors['circle'],
                        (int(pos[0]+self.tile_size/2), int(pos[1]+self.tile_size/2)),
                        int(self.tile_size/2*0.9),
                        2
                    )
                elif tile == CROSS:
                    # Where did all those fours and sixes come from?
                    pygame.draw.line(
                        self.surface,
                        self.colors['cross'],
                        (pos[0]+4, pos[1]+4),
                        (pos[0]+self.tile_size-6, pos[1]+self.tile_size-6),
                        2
                    )
                    pygame.draw.line(
                        self.surface,
                        self.colors['cross'],
                        (pos[0]+self.tile_size-6, pos[1]+4),
                        (pos[0]+4, pos[1]+self.tile_size-6),
                        2
                    )

        # Now draw the four "big" lines on the board.
        lines = (
            ((self.tile_size*3-1, 0), (self.tile_size*3-1, self.size)),
            ((self.tile_size*6-1, 0), (self.tile_size*6-1, self.size)),
            ((0, self.tile_size*3-1), (self.size, self.tile_size*3-1)),
            ((0, self.tile_size*6-1), (self.size, self.tile_size*6-1)),
        )
        for line in lines:
            pygame.draw.line(self.surface, self.colors['big'], line[0], line[1], 2)

        self.outer_surface.blit(self.surface, (self.margin, self.margin))


    def coords_to_pos(self, coords):
        """Take coordinates (from 0 to 8) and turn them into pixel positions."""
        x, y = coords
        return (x)*self.tile_size, (y)*self.tile_size


    def pos_to_coords(self, pos):
        """Take pixel positions and turn them into coordinates (from 0 to 8)."""
        x, y = pos
        return math.floor(x/self.tile_size), math.floor(y/self.tile_size)


    def set_tile(self, coords, value, force=False):
        """Set the value of the tile at coordinates to a cross or circle."""
        if force or self.tiles[coords[0]][coords[1]] is None:
            self.tiles[coords[0]][coords[1]] = value

            self.draw_board()
            return True
        return False


    def highlight_tile(self, coords):
        """Highlight the tile at specified coordinates with a chosen color."""
        # We need to draw the board first to reset all previous highlights.
        self.draw_board()

        # But, don't highlight any tiles that have a value!
        if self.tiles[coords[0]][coords[1]] is not None:
            return
        highlight = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # What's this?
        x, y = map(lambda i: i+1, self.coords_to_pos(coords))
        rect = pygame.Rect((x, y), (self.tile_size-2,)*2)
        pygame.draw.rect(highlight, self.colors['highlight'], rect, 0)

        self.surface.blit(highlight, (0, 0))
        self.outer_surface.blit(self.surface, (self.margin, self.margin))
