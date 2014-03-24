import math
import pygame
from pygame.locals import *
import warnings

DEBUG = []
DEBUG_LJUST = 15

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
        raise NotImplemented('You must write this for each piece.')



class Nought(Piece):
    def __init__(self, color):
        name = 'nought'
        abbr = 'O'
        self.size = 0.9
        super(Nought, self).__init__(name, abbr, color)
        if 'Nought' in DEBUG:
            print('Nought.__init__')
            print(self.thickness, type(self.thickness))


    def draw(self, surface, pos, size):
        """Draws the representation of a Nought."""
        if 'Nought' in DEBUG:
            print('Nought.draw')
            print('Surface'.ljust(DEBUG_LJUST), surface, type(surface))
            print('Pos'.ljust(DEBUG_LJUST), pos, type(pos), [type(x) for x in pos])
            print('Size'.ljust(DEBUG_LJUST), size, type(size))
            print('Thickness'.ljust(DEBUG_LJUST), self.thickness, type(self.thickness))
        pos = (math.ceil(pos[0] + size/2), math.ceil(pos[1] + size/2))
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
        if 'Cross' in DEBUG:
            print('Cross.draw')
            print('Surface'.ljust(DEBUG_LJUST), surface, type(surface))
            print('Pos'.ljust(DEBUG_LJUST), pos, type(pos), [type(x) for x in pos])
            print('Size'.ljust(DEBUG_LJUST), size, type(size))
            print('Thickness'.ljust(DEBUG_LJUST), self.thickness, type(self.thickness))
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


class Board(object):
    def __init__(self, pieces, tile_size, line_thickness, margin, style, n_rows=3):
        # Verify pieces
        self.pieces = []
        for piece in pieces:
            if isinstance(piece, Piece):
                self.pieces.append(piece)
            else:
                raise TypeError('All pieces must be an instance of '
                                '(a subclass of) Piece.')

        # Calculate board size
        if not tile_size % 2:
            warnings.warn('The style of the board is best with an odd tile_size.')

        self.tile_size = tile_size
        self.line_thickness = line_thickness
        self.tile_line_size = tile_size + 2 * line_thickness
        self.margin = margin
        self.n_rows = n_rows

        for name in ['tile_size', 'line_thickness', 'margin', 'n_rows']:
            attr = getattr(self, name)
            if not isinstance(attr, int):
                raise TypeError('{} must be an int, got {}.'.format(name, attr))

        self.inner_size = n_rows**2 * self.tile_line_size
        self.outer_size = self.inner_size + margin * 2

        self.highlights = []

        self.style = style
        self.reset()


    def pygame_init(self):
        self.outer_surface = pygame.Surface([self.outer_size]*2)
        self.outer_surface.fill(self.style['background-color'])

        # Draw the row and column numbers.
        font = pygame.font.Font(pygame.font.match_font(self.style['font-name']), self.style['font-size'])
        for i in range(self.n_rows**2):
            f = font.render(str(i), False, self.style['text-color'])
            rect = f.get_rect()
            rect.topleft = (
                self.tile_line_size*(i+1)-rect.width/2-self.tile_line_size/2+self.margin,
                self.margin/2-rect.height/2
            )
            self.outer_surface.blit(f, rect)
            rect.topleft = (
                self.margin/2-rect.width/2,
                self.tile_line_size*(i+1)-rect.height/2-self.tile_line_size/2+self.margin
            )
            self.outer_surface.blit(f, rect)

        self.surface = pygame.Surface([self.inner_size]*2)
        self.highlight_surf = pygame.Surface([self.inner_size]*2, pygame.SRCALPHA)
        self.draw_board()


    def reset(self):
        self.tiles = [[None]*self.n_rows**2 for i in range(self.n_rows**2)]
        self.allowed_moves = []
        for x in range(self.n_rows**2):
            self.allowed_moves.extend([(x, y) for y in range(self.n_rows**2)])
        self.turn = 0


    def draw_board(self):
        """Draw the board to the surface, with everything on it."""
        self.surface.fill(self.style['background-color'])

        for x in range(self.n_rows**2):
            for y in range(self.n_rows**2):
                # First draw the tile itself, which is just some borders.
                pos = self.coords_to_pos((x, y))
                if 'pos' in DEBUG:
                    print('Board.draw_board')
                    print('pos'.ljust(DEBUG_LJUST), pos)
                rect = pygame.Rect(pos, [self.tile_line_size]*2)
                pygame.draw.rect(
                    self.surface,
                    self.style['small-border-color'],
                    rect,
                    self.line_thickness
                )

                # Then draw a piece in it, if necessary.
                tile = self.tiles[x][y]
                pos = (pos[0] + self.line_thickness, pos[1] + self.line_thickness)
                if tile is not None:
                    tile.draw(self.surface, pos, self.tile_size)

        # Now draw the four "big" lines on the board.
        for n in range(1, self.n_rows):
            start = self.n_rows*self.tile_line_size*n - self.line_thickness
            lines = [
                ((start, 0), (start, self.inner_size)),
                ((0, start), (self.inner_size, start))
            ]

            for line in lines:
                pygame.draw.line(self.surface, self.style['big-border-color'],
                                 line[0], line[1], self.line_thickness * 2)

        self.surface.blit(self.highlight_surf, (0, 0))
        self.outer_surface.blit(self.surface, [self.margin]*2)


    def coords_to_pos(self, coords):
        """Take coordinates (from 0 to 8) and turn them into pixel positions."""
        if 'coords_to_pos' in DEBUG:
            print('Board.coords_to_pos')
            print('Coords'.ljust(DEBUG_LJUST), coords, type(coords), [type(x) for x in coords])
        x, y = coords
        return (x)*self.tile_line_size, (y)*self.tile_line_size


    def pos_to_coords(self, pos):
        """Take pixel positions and turn them into coordinates (from 0 to 8)."""
        x, y = pos
        coords = (math.floor(x/self.tile_line_size), math.floor(y/self.tile_line_size))
        if 'pos_to_coords' in DEBUG:
            print('Board.pos_to_coords')
            print('Coords'.ljust(DEBUG_LJUST), coords, type(coords), [type(x) for x in coords])
        return coords


    def switch_turns(self):
        self.turn = (self.turn + 1) % len(self.pieces)


    def update_allowed_moves(self, last_move):
        self.allowed_moves = []
        big_x, big_y = last_move[0] % self.n_rows, last_move[1] % self.n_rows
        start_x, start_y = big_x * self.n_rows, big_y * self.n_rows

        for x in range(self.n_rows):
            self.allowed_moves.extend([
                (start_x + x, start_y + y)
                for y in range(self.n_rows)
            ])

        # Remove occupied places
        for x in range(start_x, start_x + self.n_rows):
            for y in range(start_y, start_y + self.n_rows):
                if self.tiles[x][y] is not None:
                    self.allowed_moves.remove((x, y))

    def make_a_move(self, coords):
        """Add piece of whoever's turn it is to the given coordinates."""
        piece = self.pieces[self.turn]
        if self.set_tile(coords, piece):
            self.switch_turns()
            self.update_allowed_moves(coords)

            self.del_highlights(color=self.style['allowed-moves-color'])
            for move in self.allowed_moves:
                self.add_highlight(move, self.style['allowed-moves-color'])
                self.draw_highlights()
            return True
        return False


    def set_tile(self, coords, value, force=False):
        """Set the value of the tile at coordinates to given piece."""
        if force or coords in self.allowed_moves:
            if value in self.pieces:
                self.tiles[coords[0]][coords[1]] = value
            else:
                raise TypeError("Value should be one of the board's pieces.")

            self.draw_board()
            return True
        return False


    def draw_highlights(self):
        """Draw the highlights to the surface."""
        # We're gonna need to recreate the surface, otherwise old highlights
        # could "stain" it.
        self.highlight_surf = pygame.Surface([self.inner_size]*2, pygame.SRCALPHA)
        for coords, color in self.highlights:
            # Draw the highlight to the highlight surface.
            x, y = map(lambda i: i + self.line_thickness, self.coords_to_pos(coords))
            rect = pygame.Rect((x, y), (self.tile_size,)*2)
            pygame.draw.rect(self.highlight_surf, color, rect, 0)

        self.draw_board()


    def add_highlight(self, coords, color=None):
        """Highlight the tile at specified coordinates with a chosen color."""
        # Default to the style value.
        color = color or self.style['highlight-color']

        # A tuple of the color because we don't know what we're getting.
        self.highlights.append((coords, tuple(color)))


    def del_highlights(self, coords=None, color=None):
        """Delete all highlights that match the coords and/or color."""
        new_hls = self.highlights[:]
        n_deleted = 0
        for i, h in enumerate(self.highlights):
            h_coords, h_color = h

            # If coords are set, check those - same with color.
            if (coords is None or coords == h_coords) and \
               (color is None or tuple(color) == h_color):
                del new_hls[i - n_deleted]
                n_deleted = n_deleted + 1

        self.highlights = new_hls


    def get_size(self):
        return self.outer_size


    def pos_in_board(self, pos):
        x = pos[0] - self.margin
        y = pos[1] - self.margin
        if 0 < x < self.inner_size and 0 < y < self.inner_size:
            return x, y
        return False


    def get_turn_text(self):
        return str(self.pieces[self.turn])
