import asyncio
from typing import List, Set, Tuple

import numpy as np
from battleships.engine import SETTINGS, BaseAgent, Board, CellState, Ship, ShotOutcome


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
        return ",".join(
            [
                " ".join([" ".join([str(coord) for coord in x]) for x in ship])
                for ship in ships
            ]
        )

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
            elif message[0] == "U":
                shot_y, shot_x, outcome = message[1:4]
                await self.agent.handle_outcome(
                    (int(shot_y), int(shot_x)), ShotOutcome(int(outcome))
                )

                if len(message) > 4:
                    cell_state, *changes = message[4:]

                    cell_state = int(cell_state)
                    for change in changes:
                        y, x = change.split(",")
                        self.board[int(y), int(x)] = cell_state

            # unknown messages
            else:
                raise ValueError("Unknown command.")


def main(agent: BaseAgent):
    asyncio.run(GameRunner(agent).run())
