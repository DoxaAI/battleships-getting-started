from typing import List, Set, Tuple
import random

import numpy as np
from battleships import BaseAgent, ShotOutcome, main, SETTINGS
from ship_generator.random_ships_agent import generate_ships


class Agent(BaseAgent):
    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        """Returns ship cell positions to create ship objects."""
        raise NotImplementedError

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        """Makes a shot to the opponent's board at given coordinates."""
        raise NotImplementedError

    async def handle_outcome(self, shot: Tuple[int, int], outcome: ShotOutcome) -> None:
        """Handles the outcome of your last shot (optional)."""
        pass


if __name__ == "__main__":
    main(Agent())
