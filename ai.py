from pieces import AIMixin, Nought, Cross

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
