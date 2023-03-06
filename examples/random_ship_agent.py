from typing import List, Set, Tuple
import random

import numpy as np
from battleships import BaseAgent, ShotOutcome, main, Board, Ship, SETTINGS
from ship_generator.random_ships_agent import generate_ships


class RandomShipAgent(BaseAgent):
    """RandomShipAgent initializes its ships at random, using generate_ships method.
    Similarly to RandomAgent, it shoots randomly at the opponent's board."""

    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        return generate_ships(SETTINGS["ALLOWED_SHIPS"], SETTINGS["BOARD_DIMS"])

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        return (random.randint(0, 9), random.randint(0, 9))

    async def handle_outcome(self, shot: Tuple[int, int], outcome: ShotOutcome) -> None:
        pass
