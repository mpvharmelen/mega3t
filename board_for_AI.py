class Board:
    def __init__(self, n_rows):
        """
        Create a board of n_rows * n_rows big squares, which is
        n_rows ** 2 * n_rows ** 2 small tiles.

        coord (x, y) is saved in self.subtiles[x][y]
        """
        self.n_rows = n_rows
        self.reset()

    def reset(self):
        """Reset the board to play a game from the start."""
        self.subtiles = [[None]*self.n_rows**2 for i in range(self.n_rows**2)]
        # self.megatiles = [[None]*self.n_rows for i in range(self.n_rows)]

    @classmethod
    def get_lines_of_square(cls, square):
        """
        Get a list of all the rows, then all the columns and the both
        diagonals.
        """
        lines = list(square)
        lines.extend(cls.transpose_square(square))
        lines.extend(cls.diagonals_of_square(square))
        return lines

    # @classmethod
    # def add_coords_to_square(cls, square):
    #     """
    #     Return a square with coordinates add to the elements.
    #     It could be the square is translated, but the coordinates are correct.
    #     """
    #     return [
    #         [
    #             ((x, y), cls.get_tile_of_square(square, (x, y)))
    #             for y in range(len(line))
    #         ]
    #         for x, line in enumerate(square)
    #     ]

    @staticmethod
    def transpose_square(square):
        """
        Turn rows into columns and columns into rows of a given square
        """
        transpose = [list() for _ in square]
        for line in square:
            for i, el in enumerate(line):
                transpose[i].append(el)
        return transpose

    @staticmethod
    def diagonals_of_square(square):
        """
        Return both diagonals of a square.

        :return: (top left to bottom right, top right to bottom left)
        """
        diagonals = ([], [])
        for i, line in enumerate(square):
            diagonals[0].append(line[i])
            diagonals[1].append(line[len(line)-i-1])
        return diagonals

    def get_mega_square_with_coords(self, mega_coord):
        """
        Get the mega tile at the given coordinates.
        """
        square = []
        mega_x, mega_y = mega_coord
        if mega_x >= self.n_rows:
            raise ValueError(
                "Mega x-coordinate must be smaller than {}, got: {}".format(
                    self.n_rows,
                    mega_x
                )
            )
        if mega_y >= self.n_rows:
            raise ValueError(
                "Mega y-coordinate must be smaller than {}, got: {}".format(
                    self.n_rows,
                    mega_y
                )
            )
        start_x = mega_x * self.n_rows
        start_y = mega_y * self.n_rows
        for off_x in range(self.n_rows):
            x = start_x + off_x
            line = []
            square.append(line)
            for off_y in range(self.n_rows):
                y = start_y + off_y
                line.append(((x, y), self.get_tile((x, y))))
        return square

    @staticmethod
    def strip_coords_from_square(square):
        return [[el for _, el in row] for row in square]

    def set_tile(self, coords, value):
        """Set the value of the tile at coordinates to given piece."""
        self.set_tile_of_square(self.subtiles, coords, value)

    def get_tile(self, coords):
        """Get the value of the tile at coordinates."""
        return self.get_tile_of_square(self.subtiles, coords)

    @staticmethod
    def set_tile_of_square(square, coords, value):
        """Set the value of the tile at coordinates to given piece."""
        square[coords[0]][coords[1]] = value

    @staticmethod
    def get_tile_of_square(square, coords):
        """Get the value of the tile at coordinates."""
        return square[coords[0]][coords[1]]


if __name__ == '__main__':
    b = Board(3)
    for i in range(81):
        b.set_tile((i // 9, i % 9), i)
    print("Tiles: ")
    print(b.subtiles)
    for i in range(9):
        print()
        print(i)
        square = b.get_mega_square_with_coords((i // 3, i % 3))
        print("Square:")
        print(square)
        print("Lines:")
        print(b.get_lines_of_square(square))
