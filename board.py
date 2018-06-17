import math, logging
import pygame

from inherit_docstring import InheritableDocstrings

from pieces import Piece
from config import BOARD_LOGGING_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(BOARD_LOGGING_LEVEL)

class Board(object):
    def __init__(self, pieces, n_rows):
        # Verify pieces
        self.pieces = []
        for piece in pieces:
            if isinstance(piece, Piece):
                self.pieces.append(piece)
            else:
                raise TypeError('All pieces must be an instance of '
                                '(a subclass of) Piece. Got: {!r}'.format(
                                    piece))
        if isinstance(n_rows, int):
            self.n_rows = n_rows
        else:
            raise TypeError('n_rows must be an int, got {}'.format(type(n_rows)))

        self.reset()


    def reset(self):
        """Reset the board to play a game from the start."""
        self.subtiles  = [[None]*self.n_rows**2 for i in range(self.n_rows**2)]
        self.megatiles = [[None]*self.n_rows    for i in range(self.n_rows)]

        self.clear_allowed_moves()
        for x in range(self.n_rows**2):
            self.allowed_moves.extend([(x, y) for y in range(self.n_rows**2)])

        self.winning_lines = []
        self.game_over = False
        self.turn = 0


    def get_turn(self):
        return self.pieces[self.turn]


    def switch_turns(self):
        """Switch turns"""
        self.turn = (self.turn + 1) % len(self.pieces)


    def check_for_draw(self):
        """Check if there is a draw and update the board accordingly"""
        if len(self.allowed_moves):
            return False
        # If there are no allowed moves, there is a draw
        logger.info('Draw!')
        return True


    def find_winner(self, last_piece, last_move):
        """
        Check if someone won a megatile and maybe even the whole game!
        Also updates self.megatiles.

        Didn't win:
            obj.find_winner(last_piece, last_move) -> ()
        Won megatile (but not game):
            obj.find_winner(last_piece, last_move) -> ((area, line),)
        Won game:
            obj.find_winner(last_piece, last_move) -> ((area, line), line)
        """
        # You only have to check the last megatile someone played in,
        # because you can't win anywhere else (and otherwise we would have
        # already noticed).

        winning_info = self.find_winner_megatile(last_piece, last_move)
        if winning_info is None:
            return ()

        area_coords = winning_info[0]
        logger.info('{} won megatile {}'.format(last_piece, area_coords))
        self.megatiles[area_coords[0]][area_coords[1]] = last_piece

        # Check for game
        big_winning_line = self.check_has_line(last_piece, area_coords, self.megatiles)
        if big_winning_line is not None:
            logger.info('{} won the game!'.format(last_piece))
            return (winning_info, big_winning_line)
        else:
            return (winning_info,)


    def find_winner_megatile(self, last_piece, last_move):
        """
        Check if someone won a megatile.


        obj.check_winner(last_move) -> (area_coords, winning_line) or None
        """
        # Coordinates of megatile in self.megatiles
        big_x = int(last_move[0] / self.n_rows)
        big_y = int(last_move[1] / self.n_rows)

        # Starting coordinates of megatile in self.subtiles
        start_x = big_x * self.n_rows
        start_y = big_y * self.n_rows

        # Coords of last_move in megatile:
        small_coords = (last_move[0] % self.n_rows, last_move[1] % self.n_rows)

        # Create working area
        working_grid = []
        for x in range(self.n_rows):
            working_grid.append([
                self.get_tile((start_x + x, start_y + y))
                for y in range(self.n_rows)
            ])

        winning_line = self.check_has_line(last_piece, small_coords, working_grid)
        return None if winning_line is None else ((big_x, big_y), winning_line)


    def check_has_line(self, last_piece, last_move, grid):
        """
        Check if the last move was a winning one.

        obj.check_has_line(last_move, grid) -> winning_coords or None
        """
        possibilities = []

        # Column
        possibilities.append(
            ([(last_move[0], y) for y in range(self.n_rows)],
            [grid[last_move[0]][y] for y in range(self.n_rows)])
        )

        # Row
        possibilities.append(
            ([(x, last_move[1]) for x in range(self.n_rows)],
            [grid[x][last_move[1]] for x in range(self.n_rows)])
        )

        # Diagonal (-- to ++)
        if last_move[0] == last_move[1]:
            possibilities.append(
                ([(co, co) for co in range(self.n_rows)],
                [grid[co][co] for co in range(self.n_rows)])
            )

        # Diagonal (-+ to +-)
        if last_move[0] == self.n_rows - 1 - last_move[1]:
            possibilities.append(
                ([(co, -co - 1) for co in range(self.n_rows)],
                [grid[co][-co - 1] for co in range(self.n_rows)])
            )

        other_pieces = self.pieces.copy()
        while last_piece in other_pieces:
            other_pieces.remove(last_piece)
        winning_coords = []
        has_won = False
        for coords, poss in possibilities:
            if None in poss:
                continue
            has_won = True
            for piece in other_pieces:
                if piece in poss:
                    has_won = False
                    break
            if has_won:
                winning_coords = []
                for co in coords:
                    winning_coords.append([co[0] % self.n_rows, co[1] % self.n_rows])
                break
        return winning_coords or None


    def make_a_move(self, coords, forced=False):
        """
        Add piece of whoever's turn it is to the given coordinates.

        Returns whether the move was legal
        """
        piece = self.get_turn()
        if self.set_tile(coords, piece, forced):
            if len(self.find_winner(piece, coords)) > 1:
                # Someone won the game
                self.game_over = True
                self.clear_allowed_moves()
                return True

            self.switch_turns()
            self.update_allowed_moves(coords)

            if self.check_for_draw():
                self.game_over = True
                self.clear_allowed_moves()
            return True
        return False


    def clear_allowed_moves(self):
        self.allowed_moves = []


    def update_allowed_moves(self, last_move):
        self.clear_allowed_moves()
        big_x, big_y = last_move[0] % self.n_rows, last_move[1] % self.n_rows
        if self.megatiles[big_x][big_y] is None:
            # Play withing this megatile
            self.allowed_moves = self.get_empty_subtiles((big_x, big_y))
            if self.allowed_moves:
                # There are allowed moves
                return

        # This megatile was occupied or
        # There were no allowed moves
        # >> play anywhere
        for x in range(self.n_rows):
            for y in range(self.n_rows):
                if self.megatiles[x][y] is None:
                    allowed_moves = self.get_empty_subtiles((x, y))
                    self.allowed_moves.extend(allowed_moves)


    def get_empty_subtiles(self, big_coords):
        empty = []
        start_x, start_y = big_coords[0] * self.n_rows, big_coords[1] * self.n_rows

        for x in range(self.n_rows):
            empty.extend([
                (start_x + x, start_y + y)
                for y in range(self.n_rows)
                if self.get_tile((start_x + x, start_y + y)) is None
            ])

        return empty


    def set_tile(self, coords, value, forced=False):
        """Set the value of the tile at coordinates to given piece."""
        if forced or coords in self.allowed_moves:
            if value in self.pieces:
                self.subtiles[coords[0]][coords[1]] = value
            else:
                raise ValueError("Value should be one of the board's pieces.")
            return True
        return False


    def get_tile(self, coords):
        return self.subtiles[coords[0]][coords[1]]



class AIBoard(Board):
    """API for AI players."""
    def __init__(self, *args, **kwargs):
        logger.debug('args: {}'.format(args))
        logger.debug('kwargs: {}'.format(kwargs))
        self.mutations = {}
        super(AIBoard, self).__init__(*args, **kwargs)
        self.mutations = {piece: [] for piece in self.pieces if piece.is_AI()}
        self.reset()

    def reset(self):
        """Reset the board"""
        super(AIBoard, self).reset()
        for ai in self.mutations:
            ai.save_board_info(self.n_rows, self.pieces)

    def add_mutation(self, coords, piece):
        for ai in self.mutations:
            self.mutations[ai].append((coords, piece))


    def get_mutations(self, ai):
        if ai in self.mutations:
            out = self.mutations[ai]
            self.mutations[ai] = []
            return out
        else:
            raise ValueError("{} not in known AIs".format(ai))


    def make_a_move(self, coords, *args, **kwargs):
        player = self.get_turn()
        if super(AIBoard, self).make_a_move(coords, *args, **kwargs):
            self.add_mutation(coords, player)
            return True
        return False



class PygameBoard(AIBoard, metaclass=InheritableDocstrings):
    def __init__(self, pieces, tile_size, line_thickness, margin, style, n_rows):
        super(PygameBoard, self).__init__(pieces, n_rows)

        # Calculate board size
        if not tile_size % 2:
            logger.warn('The style of the board is best with an odd tile_size.')

        self.tile_size = tile_size
        self.line_thickness = line_thickness
        self.tile_line_size = tile_size + 2 * line_thickness
        self.margin = margin

        for name in ['tile_size', 'line_thickness', 'margin']:
            attr = getattr(self, name)
            if not isinstance(attr, int):
                raise TypeError('{} must be an int, got {}.'.format(name, type(attr)))

        self.inner_size = n_rows**2 * self.tile_line_size
        self.outer_size = self.inner_size + margin * 2

        self.style = style


    def pygame_init(self):
        """Initialize everything to do with pygame."""
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

    @copy_ancestor_docstring
    def reset(self):
        super(PygameBoard, self).reset()
        self.highlights = []


    def draw_board(self):
        """Draw the board to the surface, with everything on it."""
        self.surface.fill(self.style['background-color'])

        for x in range(self.n_rows**2):
            for y in range(self.n_rows**2):
                # First draw the tile itself, which is just some borders.
                pos = self.coords_to_pos((x, y))

                logger.debug('PygameBoard.draw_board')
                logger.debug('{}, {}'.format('pos', pos))

                rect = pygame.Rect(pos, [self.tile_line_size]*2)
                pygame.draw.rect(
                    self.surface,
                    self.style['small-border-color'],
                    rect,
                    self.line_thickness
                )

                # Then draw a piece in it, if necessary.
                tile = self.get_tile((x, y))
                pos = (pos[0] + self.line_thickness, pos[1] + self.line_thickness)
                if tile is not None:
                    tile_surface = pygame.Surface([self.tile_size]*2)
                    tile_surface.fill(self.style['background-color'])
                    tile.draw(tile_surface)
                    self.surface.blit(tile_surface, pos)

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

        for line in self.winning_lines:
            pygame.draw.line(
                self.highlight_surf,
                self.style['winning-line-color'],
                line[0],
                line[1],
                self.style['winning-line-thickness']
            )
            for end in line:
                pygame.draw.circle(self.highlight_surf,
                    self.style['winning-line-color'],
                    end,
                    self.style['winning-line-thickness'] // 2,
                    0
                )

        self.surface.blit(self.highlight_surf, (0, 0))
        self.outer_surface.blit(self.surface, [self.margin]*2)


    def coords_to_pos(self, coords):
        """
        Take coordinates (from 0 to n_rows ** 2 - 1) and turn them into pixel positions.
        """
        logger.debug('PygameBoard.coords_to_pos')
        logger.debug('{}, {}, {}, {}'.format('Coords', coords, type(coords), [type(x) for x in coords]))
        x, y = coords
        return (x)*self.tile_line_size, (y)*self.tile_line_size


    def pos_to_coords(self, pos):
        """Take pixel positions and turn them into coordinates (from 0 to n_rows ** 2 - 1)."""
        x, y = pos
        coords = (int(math.floor(x/self.tile_line_size)), int(math.floor(y/self.tile_line_size)))
        logger.debug('PygameBoard.pos_to_coords')
        logger.debug('{}, {}, {}, {}'.format('Coords', coords, type(coords), [type(x) for x in coords]))
        return coords


    def find_winner(self, last_piece, last_move):
        """
        Check if someone won a megatile and maybe even the whole game!
        Also updates self.megatiles and self.highlights accordingly.
        """
        lines = super(PygameBoard, self).find_winner(last_piece, last_move)
        if lines:
            area_coords = lines[0][0]
            winning_line = lines[0][1]
            # Didn't feel like writing a loop for this... am I lazy yet?
            realify = lambda coords: [c + (self.n_rows * area_coords[i]) for i, c in enumerate(coords)]
            real_line = tuple(map(realify, winning_line))

            self.draw_line(real_line)

            # Highlight megatile
            for x in range(self.n_rows):
                for y in range(self.n_rows):
                    coords = realify([x, y])
                    self.add_highlight(coords, last_piece.color + (self.style['winning-highlight-alpha'],))

            if len(lines) > 1:
                realify = lambda coords: [int((c + 0.5) * self.n_rows) for c in coords]
                big_line = tuple(map(realify, lines[1]))
                self.draw_line(big_line)
        return lines


    @copy_ancestor_docstring
    def make_a_move(self, coords, forced=False):
        legal = super(PygameBoard, self).make_a_move(coords, forced)
        if legal:
            self.del_highlights(color=self.style['last-move-color'])
            self.add_highlight(coords, self.style['last-move-color'])
            self.draw_highlights()
        return legal


    @copy_ancestor_docstring
    def clear_allowed_moves(self):
        super(PygameBoard, self).clear_allowed_moves()
        if getattr(self, 'highlights', False):
            self.del_highlights(color=self.style['allowed-moves-color'])


    @copy_ancestor_docstring
    def update_allowed_moves(self, last_move):
        super(PygameBoard, self).update_allowed_moves(last_move)
        for move in self.allowed_moves:
            self.add_highlight(move, self.style['allowed-moves-color'])


    def draw_line(self, line):
        """Draw a line from line[0] to line[-1]."""
        # Add points for line drawing from/to middle of subtiles.
        start = self.coords_to_pos(line[0])
        end = self.coords_to_pos(line[-1])

        half_tile = int(self.tile_size/2)
        start = start[0] + half_tile, start[1] + half_tile
        end = end[0] + half_tile, end[1] + half_tile

        line = [start, end]
        self.winning_lines.append(line)


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

    def add_highlight(self, coords, color=None):
        """Highlight the tile at specified coordinates with a chosen color."""
        # Default to the style value.
        color = color or self.style['highlight-color']
        self.highlights.append((coords, color))


    def del_highlights(self, coords=None, color=None):
        """Delete all highlights that match the coords and/or color."""
        new_hls = self.highlights.copy()
        n_deleted = 0
        for i, h in enumerate(self.highlights):
            h_coords, h_color = h

            # If coords are set, check those - same with color.
            if (coords is None or coords == h_coords) and \
               (color is None or tuple(color) == tuple(h_color)):
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
        return str(self.get_turn())
