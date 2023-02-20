import asyncio
from enum import IntEnum
from typing import List, Set, Tuple

import numpy as np


class ShotOutcome(IntEnum):
    MISS = 0
    HIT = 1
    DESTROYED = 2
    REPEATED_SHOT = 3
    INVALID_SHOT = 4


class BaseAgent:
    """A base Battleships agent."""

    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        raise NotImplementedError

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        raise NotImplementedError

    async def handle_outcome(self, shot: Tuple[int, int], outcome: ShotOutcome) -> None:
        pass


class GameRunner:
    def __init__(self, agent: BaseAgent) -> None:
        self.agent = agent

    def _handle_initialisation(self):
        message = input().strip()
        assert message.startswith("INIT")

        _, y, x = message.split(" ")
        self.board = np.zeros((int(y), int(x)))

        print("OK")

    def _encode_ships(self, ships: List[Set[Tuple[int, int]]]) -> str:
        # TODO: implement a way to encode ships
        raise NotImplementedError

    async def run(self):
        self._handle_initialisation()

        while True:
            message = input().strip().split(" ")

            # initial board ship placement
            if message[0] == "B":
                ships = await self.agent.get_ships()
                print(self._encode_ships(ships))

            # making shots
            elif message[0] == "S":
                print(*(await self.agent.shoot(self.board)))

            # handling state updates
            elif message[0] == "U" and len(message) >= 5:
                shot_y, shot_x, outcome, cell_state, *changes = message

                # TODO: check if this is the right order we want
                self.agent.handle_outcome((shot_x, shot_y), ShotOutcome(int(outcome)))

                cell_state = int(cell_state)
                for change in changes:
                    y, x = change.split(",")
                    self.board[int(y), int(x)] = cell_state

            # unknown messages
            else:
                raise ValueError("Unknown command.")


def main(agent: BaseAgent):
    asyncio.run(GameRunner(agent).run())