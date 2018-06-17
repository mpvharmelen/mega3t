"""
The action space is the the coordinates.
The agent will get a big punishment if it makes an illegal move and the
environment will be reset.

It will first play against a RandomAI
"""
from collections import Counter
from gym import Env, spaces
from board import AIBoard
from pieces import Cross, NoughtAI
from constants import CROSS_COLOR, NOUGHT_COLOR


class Mega3TEnv(Env):
    def __init__(
            self,
            piece=Cross(CROSS_COLOR),
            opponents=[NoughtAI(NOUGHT_COLOR)],
            n_rows=3):
        self.piece = piece
        self.opponents = opponents
        self.n_rows = n_rows
        self.reset()

        # action        (mega x, mega y, small x, small y)
        self.action_space = spaces.MultiDiscrete([n_rows] * 4)

        # observation   (player, ) * (n_rows ** 2) ** 2
        # self.observation_space = spaces.MultiDiscrete(
        #     [len(opponents) + 2] * (n_rows ** 2) ** 2
        # )

        # observation   ((((player, ) * n_rows) * n_rows) * n_rows) * n_rows
        self.observation_space = spaces.Tuple(
            spaces.Tuple(
                spaces.Tuple(
                    spaces.MultiDiscrete([len(opponents) + 2] * n_rows)
                    for _ in range(n_rows)
                )
                for _ in range(n_rows)
            )
            for _ in range(n_rows)
        )

    def reset(self):
        self.board = AIBoard([self.piece] + self.opponents, self.n_rows)
        return self.get_obs()

    def move_others(self):
        last_move = None
        for opp in self.opponents:
            # Don't do anything if the game is over
            if self.board.game_over:
                break
            done = False
            while not done:
                last_move = opp.move(
                        self.board.get_mutations(opp),
                        self.board.allowed_moves
                    )
                done = self.board.make_a_move(last_move)
        # Return the last move that was made
        return opp, last_move

    def action_to_coords(self, action):
        mega_x, mega_y, tiny_x, tiny_y = action
        return (
            mega_x * self.n_rows + tiny_x,
            mega_y * self.n_rows + tiny_y
        )

    def step(self, action):
        reward = 0.0
        WIN_REWARD = 1.0
        LOSE_REWARD = -1.0
        ILLEGAL_REWARD = LOSE_REWARD
        DRAW_REWARD = 0.0
        WIN_MEGA_TILE_REWARD = 0.1
        LOSE_MEGA_TILE_REWARD = -0.05

        coords = self.action_to_coords(action)
        tiles_free = self.board.megatiles.count(None)
        legal = self.board.make_a_move(coords)
        if not legal:
            # Very bad!
            reward = ILLEGAL_REWARD
            # Reset
            done = True
            # Exit
            return (self.get_obs(), reward, done, {})

        if tiles_free > self.board.megatiles.count(None):
            # We won a mega tile!
            # Small reward
            reward = WIN_MEGA_TILE_REWARD
            if len(self.board.find_winner(self.piece, coords)) > 1:
                # We won the game!!
                # Big reward
                reward = WIN_REWARD

        tiles_free = self.board.megatiles.count(None)
        # `move_others` checks whether the game is over before playing
        last_move = self.move_others()

        if tiles_free > self.board.megatiles.count(None):
            reward = LOSE_MEGA_TILE_REWARD

        if self.board.game_over:
            if last_move is not None and \
               len(self.board.find_winner(*last_move)) > 1:
                # We lost the game!!
                # Very bad
                reward = LOSE_REWARD
            else:
                # Board is full
                most_common = Counter(
                    map(self.board_value_to_int, self.board.megatiles)
                ).most_common()
                drawers = [p for p, v in most_common if v == most_common[0][0]]
                my_value = self.board_value_to_int(self.piece)
                if len(drawers) == 1:
                    # Someone won
                    if drawers[0] == my_value:
                        # We won because we have more mega squares
                        reward = WIN_REWARD
                    else:
                        # We lost because someone else has more mega squares
                        reward = LOSE_REWARD
                else:
                    # A draw
                    if my_value in drawers:
                        # We drew because we have the same number of mega
                        # squares as someone else
                        reward = DRAW_REWARD
                    else:
                        # We lost because someone others had more mega squares
                        reward = LOSE_REWARD

        return (self.get_obs(), reward, self.board.game_over, {})

    def get_obs(self):
        """
        Convert the board to an observation
        """
        mega_block = []
        for mega_x in range(self.n_rows):
            mega_row = []
            mega_block.append(mega_row)
            for mega_y in range(self.n_rows):
                tiny_block = []
                mega_row.append(tiny_block)
                for tiny_x in range(self.n_rows):
                    x = mega_x * self.n_rows + tiny_x
                    tiny_row = []
                    tiny_block.append(tiny_row)
                    for tiny_y in range(self.n_rows):
                        y = mega_y * self.n_rows + tiny_y
                        tiny_row.append(
                            self.board_value_to_int(
                                self.board.get_tile((x, y))
                            )
                        )
        return mega_block

    def board_value_to_int(self, value):
        if value is None:
            return 0
        if value == self.piece:
            return 1
        return self.opponents.index(value) + 2


if __name__ == '__main__':
    env = Mega3TEnv()
    print(env.reset())
    # Legal move
    print(env.step((0, 0, 0, 0)))
    # Illegal move
    print(env.step((0, 0, 0, 0)))