import random
from typing import List, Set, Tuple

import numpy as np
from battleships import SETTINGS, BaseAgent, Board, Ship, ShotOutcome, main


class RandomAgent(BaseAgent):
    """Random agent shoots randomly at the opponent's board."""

    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        return [
            {(2, 3)},
            {(5, 8)},
            {(0, 5)},
            {(4, 2)},
            {(1, 7), (2, 7)},
            {(6, 6), (7, 6)},
            {(4, 5), (4, 6)},
            {(2, 9), (3, 9), (1, 9)},
            {(8, 3), (8, 4), (9, 4)},
            {(6, 1), (8, 1), (7, 1), (6, 0)},
        ]

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        return (random.randint(0, 9), random.randint(0, 9))

    async def handle_outcome(self, shot: Tuple[int, int], outcome: ShotOutcome) -> None:
        pass
