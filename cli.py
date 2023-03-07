import asyncio
import os
import sys
import time
from typing import List, Set, Tuple

import numpy as np

sys.path.append(os.path.dirname(os.path.abspath("submission/agent.py")))
sys.path.append(os.path.dirname(os.path.abspath("submission/battleships")))
sys.path.append(os.path.dirname(os.path.abspath("examples/random_agent.py")))


from submission.agent import Agent
from submission.battleships.engine import BaseAgent, Game

# from examples.random_agent import RandomAgent


class BattleshipsCLI:
    def __init__(self) -> None:
        pass

    async def run(self, game: Game) -> None:
        """Runs the game for the CLI UI.

        Args:
            game (Game): The Battleships game.
        """
        player = 0
        shot_number = 0
        async for player, shot, outcome, _, _ in game.run():
            if player == 0:
                await game.player1.handle_outcome(shot, outcome)

                print(
                    f"Your move: ({shot[0]}, {shot[1]}).",
                    f"Outcome: {outcome.name}.",
                    "\nYour agent's board",
                    "=" * 21,
                    sep="\n",
                )
                print(game.board2)

            else:
                await game.player2.handle_outcome(shot, outcome)
                print(
                    f"Your agent's move: ({shot[0]}, {shot[1]}).",
                    f"Outcome: {outcome.name}.",
                    "\nYour board",
                    "=" * 21,
                    sep="\n",
                )
                print(game.board1)
                print("*" * 40 + "\n")
                shot_number += 1
                time.sleep(0.01)

        print(
            f"{'You' if player == 0 else 'Your agent'} won after {shot_number} shots!"
        )


async def main():
    ui = BattleshipsCLI()

    # Uncomment the following line to run a game between two different agents
    # await ui.run(Game(Agent(), Agent()))

    # Play using keyboard against your agent
    await ui.run(Game(HumanAgent(), Agent()))


class HumanAgent(BaseAgent):
    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        message = input("Your ships: ").strip()

        try:
            return [
                {(int(ship[i]), int(ship[i + 2])) for i in range(0, len(ship), 4)}
                for ship in message.split(",")
            ]
        except:
            raise ValueError("Something went wrong while getting your ships.")

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        message = input("Your move: ").strip().split(" ")

        x, y = int(message[0]), int(message[1])

        return x, y


if __name__ == "__main__":
    asyncio.run(main())
