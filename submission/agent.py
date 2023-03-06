from typing import List, Set, Tuple

import numpy as np
from battleships import SETTINGS, BaseAgent, ShotOutcome, main

# from battleships.random_ship_generator import generate_ships


#################################################################
#   Modify the Agent class below to implement your own agent.   #
#   You may define additional methods as you see fit.           #
#################################################################


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
