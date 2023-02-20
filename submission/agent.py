from typing import List, Set, Tuple

import numpy as np
from battleships import BaseAgent, ShotOutcome, main


class Agent(BaseAgent):
    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        raise NotImplementedError

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        raise NotImplementedError

    async def handle_outcome(self, shot: Tuple[int, int], outcome: ShotOutcome) -> None:
        pass


if __name__ == "__main__":
    main(Agent())
