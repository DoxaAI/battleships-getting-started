from collections import deque
from enum import IntEnum
from typing import Any, AsyncGenerator, Deque, Dict, List, Literal, Optional, Set, Tuple

import numpy as np
from battleships.exceptions import (
    InvalidShipException,
    InvalidShipsCountException,
    ShipRegistrationException,
)

SETTINGS: Dict[str, Any] = {
    "BOARD_DIMS": (10, 10),
    "ALLOWED_SHIPS": {1: 4, 2: 3, 3: 2, 4: 1},
}


class CellState(IntEnum):
    EMPTY = 0
    HEALTHY = 1
    MISS = 2
    HIT = 3
    DESTROYED = 4


class ShotOutcome(IntEnum):
    MISS = 0
    HIT = 1
    DESTROYED = 2
    REPEATED_SHOT = 3
    INVALID_SHOT = 4


class ShipState(IntEnum):
    DESTROYED = 0
    DAMAGED = 1
    HEALTHY = 2


class Ship:
    """Representation of a ship.

    Ship is defined by a set of cells and its state. Once ship is being damaged,
    the _shots_taken value is increased.
    Once it matches _ship_size, the ship is destroyed.


    Attributes:
        ship_cells (Set[Tuple[int, int]]): coordinates of cells constituting a ship.
        state (ShipState): State of a ship object.
        _ship_size (int): Number of ship cells.
        _shots_taken (int): Number of shots taken by the ship.
    """

    ship_cells: Set[Tuple[int, int]]
    state: ShipState
    _ship_size: int
    _shots_taken: int

    def __init__(self, ship_cells: Set[Tuple[int, int]]) -> None:
        self.ship_cells = set(ship_cells)
        self._ship_size = len(ship_cells)
        self._shots_taken = 0
        self.state = ShipState.HEALTHY
        self.validate()

    def damage(self) -> None:
        """Damages a ship.

        Increases the number of shots taken by the ship.
        Changes ship state appropriately.
        """
        self._shots_taken += 1
        if self._shots_taken == self._ship_size:
            self.state = ShipState.DESTROYED
        else:
            self.state = ShipState.DAMAGED

    def validate(self) -> None:
        """Validates ship cells.

        Checks whether ship cells have positive coords and whether they
        create a connected component.

        Raises:
            InvalidShipException: Ship cells create an invalid ship.
        """
        # all cells need to have positive coords
        for x, y in self.ship_cells:
            if x < 0 or y < 0:
                raise InvalidShipException(
                    f"Ship with negative coordinates not allowed {(x, y)}"
                )

        # check if ship cells create a connected component
        if not self.connected_bfs():
            raise InvalidShipException(f"Ship with illegally placed cells")

    def connected_bfs(self) -> bool:
        """Checks whether all ship cells are connected.

        Uses BFS implementation, which does not check for potential (negative)
        boundaries when considering neighboring cells.

        Returns:
            bool: True if cells are connected, False otherwise.
        """
        cell_list: List[Tuple[int, int]] = list(self.ship_cells)
        q: Deque[Tuple[int, int]] = deque()
        visited: Set[Tuple[int, int]] = {cell_list[0]}
        q.appendleft(cell_list[0])
        while q:
            c_node: Tuple[int, int] = q.pop()
            tmp_nodes: List[Tuple[int, int]] = [
                (c_node[0] - 1, c_node[1]),
                (c_node[0] + 1, c_node[1]),
                (c_node[0], c_node[1] + 1),
                (c_node[0], c_node[1] - 1),
            ]
            for tmp_node in tmp_nodes:
                if tmp_node in cell_list and tmp_node not in visited:
                    q.appendleft(tmp_node)
                    visited.add(tmp_node)

        return visited == self.ship_cells


class Board:
    """Player's board with ships.

    Board is an array of size nxm (specified in size). Each cell in the array has a CellState.
    Board also stores all the ships it contains in the ships dictionary,

    Attributes:
        size (Tuple[int, int]): size of a board.
        ships_cells (Dict[Tuple[int, int], Ship]): Maps positions to ship references.
        board (np.ndarray): array of *size* representing the board.
    """

    size: Tuple[int, int]
    ships_cells: Dict[Tuple[int, int], Ship]
    board: np.ndarray

    def __init__(self, size: Tuple[int, int]) -> None:
        self.size = size
        self.ships_cells = {}
        self.board = np.zeros(size)

    def _register_ship(self, ship: Ship) -> None:
        """Registers a single ship on the Board if it can be registered.

        Args:
            ship (Ship): Ship object to register.

        Raises:
            ShipRegistrationException: When ship cannot be registered on the Board.
        """
        self._validate_registration(ship)

        for cell in ship.ship_cells:
            self.ships_cells[cell] = ship
            self.board[cell] = CellState.HEALTHY

    def _validate_registration(self, ship: Ship) -> None:
        """Checks if a given ship can be registered on the Board.

        Args:
            ship (Ship): Ship object to register.

        Raises:
            ShipRegistrationException: When ship cannot be registered on the Board.
        """
        for cell in ship.ship_cells:
            if cell[0] >= self.size[0] or cell[1] >= self.size[1]:
                raise ShipRegistrationException(
                    f"Ship Cell {cell}" f" outside the board!"
                )

            if self.board[cell] == CellState.HEALTHY:
                raise ShipRegistrationException(
                    f"Ship cell {cell} already " f"occupied by another ship!"
                )

            outcome: Optional[Tuple[int, int]] = self._is_ship_too_close(cell)
            if outcome is not None:
                raise ShipRegistrationException(
                    f"Ship cell {cell} too close to"
                    f" a cell of another ship {outcome}!"
                )

    def _is_ship_too_close(self, cell: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Checks if there are no nearby ships at a desired registration cell.

        Ship cell cannot be placed if any of 8 surrounding cells is occupied by another ship.

        Args:
            cell (Tuple[int, int]): coordinates of a desired ship registration cell.

        Returns:
            None if ship cell can be safely placed in a desired location.
            Otherwise, returns Tuple[int, int] indicating coordinates of a cell
                blocking the registration.
        """
        y, x = cell
        cells_to_check: Set[Tuple[int, int]] = {
            (y - 1, x),
            (y - 1, x + 1),
            (y, x + 1),
            (y + 1, x + 1),
            (y + 1, x),
            (y + 1, x - 1),
            (y, x - 1),
            (y - 1, x - 1),
        }

        for coord in cells_to_check:
            if (
                coord[0] < 0
                or coord[0] >= self.size[0]
                or coord[1] < 0
                or coord[1] >= self.size[1]
            ):
                continue

            if self.board[coord] == CellState.HEALTHY:
                return coord

        return None

    def register_ships(self, ships_list: List[Ship]) -> None:
        """Registers all given ships on the Board.

        Args:
            ships_list (List[Ship]): List containing ship objects to be registered.

        Raises:
            ShipRegistrationException: When one or more ships cannot be registered.
        """

        for ship in ships_list:
            self._register_ship(ship)

    def shoot(
        self, cell: Tuple[int, int]
    ) -> Tuple[ShotOutcome, Optional[CellState], List[Tuple[int, int]]]:
        """Performs a shot at a desired location.

        Args:
            cell (Tuple[int, int]): coordinates of a desired location of a shot.

        Returns:
            Tuple of:
            - ShotOutcome representing shot outcome,
            - CellState if the cell state was changed otherwise None,
            - List of cell coordinates with changed states.
        """
        # check if shot in the board range.
        if (
            cell[0] < 0
            or cell[1] < 0
            or cell[0] > self.size[0] - 1
            or cell[1] > self.size[1] - 1
        ):
            return ShotOutcome.INVALID_SHOT, None, []

        cell_state = self.board[cell]

        # if player shoots in the same cell as before
        if cell_state in (CellState.HIT, CellState.DESTROYED, CellState.MISS):
            return ShotOutcome.REPEATED_SHOT, None, []

        # missed
        if cell_state == CellState.EMPTY:
            self.board[cell] = CellState.MISS
            return ShotOutcome.MISS, CellState.MISS, [cell]

        ship: Ship = self.ships_cells[cell]
        ship.damage()

        # respond with appropriate message
        if ship.state == ShipState.DAMAGED:
            self.board[cell] = CellState.HIT
            return ShotOutcome.HIT, CellState.HIT, [cell]

        # if destroyed, mark all ships cells as destroyed.
        for cell in ship.ship_cells:
            self.board[cell] = CellState.DESTROYED

        return ShotOutcome.DESTROYED, CellState.DESTROYED, list(ship.ship_cells)

    def get_masked_board(self) -> np.ndarray:
        """Returns a copy of the board with ship cells with masked ships.

        Returns:
            A copy of np.ndarray representing a board with CellState.HEALTHY turned into CellState.EMPTY.
        """
        masked_board: np.ndarray = self.board.copy()
        masked_board[masked_board == CellState.HEALTHY] = CellState.EMPTY
        return masked_board

    def __repr__(self) -> str:
        """Encodes player's board."""

        board: str = "  "
        for i in range(self.size[1]):
            board += str(i) + " "

        board += "\n"
        for i in range(self.size[0]):
            board += str(i) + " "
            for j in range(self.size[1]):
                char_to_print: Literal["O", "-", ".", "X"] = "O"
                if self.board[(i, j)] == CellState.EMPTY:
                    char_to_print = "-"
                elif self.board[(i, j)] == CellState.MISS:
                    char_to_print = "."
                elif self.board[(i, j)] in (CellState.HIT, CellState.DESTROYED):
                    char_to_print = "X"
                board += char_to_print + " "
            board += "\n"

        return board

    def get_existing_ships_count(self) -> int:
        return sum(
            [bool(ship.state) for ship in {ship for ship in self.ships_cells.values()}]
        )


class BaseAgent:
    """A base agent."""

    async def get_ships(self) -> List[Set[Tuple[int, int]]]:
        """Returns coordinates of ship cells to create ship objects.

        E.g. 2 ships of 1 cell (1,1 and 8,8), 1 ship of 3 (3,4 3,5 3,6) cells will be encoded as follows:
        [{(1, 1)}, {(8, 8)}, {(3, 4), (3, 5), (3, 6)}]

        Returns:
            List[Set[Tuple[int, int]]], where each Tuple[int, int] represents a ship cell coordinate,
                Set of Tuples is a full ship and List of Sets is a list of all desired ships.
        """
        raise NotImplementedError

    async def shoot(self, board: np.ndarray) -> Tuple[int, int]:
        """Performs a shot to the opponent's board.

        Shot in coordinates 3, 3 will be represented by a tuple
        (3,3). Additionally, gets a masked opponent's board as an argument.

        Args:
            board (np.ndarray): Current state of the opponent's board.
                Unknown ships are masked by CellState.EMPTY values.

        Returns:
            A Tuple[int, int] representing the coordinates of a desired shot.
        """
        raise NotImplementedError

    async def handle_outcome(self, shot: Tuple[int, int], outcome: ShotOutcome) -> None:
        """Handles the outcome of your last shot (optional).

        Args:
            shot (Tuple[int, int]): Coordinates of agent's previous shot.
            outcome (ShotOutcome): The outcome of the previous agent's shot.
        """
        pass


class Game:
    """Game controller.

    Manages player's ship registration and game logic.

    Attributes:
        player1 (Player): First player.
        player2 (Player): Second player.
    """

    player1: BaseAgent
    player2: BaseAgent

    def __init__(self, player1: BaseAgent, player2: BaseAgent) -> None:
        self.player1 = player1
        self.player2 = player2

        self.board1 = Board(SETTINGS["BOARD_DIMS"])
        self.board2 = Board(SETTINGS["BOARD_DIMS"])

    async def initialize(self) -> None:
        """Initialize the game."""
        self.board1.register_ships(await self._get_ships(self.player1))
        self.board2.register_ships(await self._get_ships(self.player2))

    async def _get_ships(self, player: BaseAgent) -> List[Ship]:
        """Get ships from an agent.

        Args:
            player (BaseAgent): player's implementation of an Agent.

        Returns:
            A List[Ship] list of ships player wants to add to the board.
        """
        ships = await player.get_ships()

        self._check_ships_count(ships)

        return [Ship(ship) for ship in ships]

    def _is_game_running(self) -> bool:
        """Checks is the game still running.

        Returns:
            True if the game is still running, False otherwise.
        """
        return (
            self.board1.get_existing_ships_count() > 0
            and self.board2.get_existing_ships_count() > 0
        )

    def _check_ships_count(self, ship_list: List[Set[Tuple[int, int]]]) -> None:
        """Checks that the user's input matches ship number and size requirements.

        Args:
            ship_list (List[Set[Tuple[int, int]]]): A list of ships to be validated.

        Raises:
            InvalidShipsCountException: If the number and sizes of given ships
                are different than specified in SETTINGS.
        """

        ships_count: Dict[int, int] = {}
        for ship in ship_list:
            try:
                ships_count[len(ship)] += 1
            except KeyError:
                ships_count[len(ship)] = 1

        if ships_count != SETTINGS["ALLOWED_SHIPS"]:
            raise InvalidShipsCountException(
                "The number of ships within classes don't match the requirements. Oops..."
            )

    async def run(
        self,
    ) -> AsyncGenerator[
        Tuple[
            int,
            Tuple[int, int],
            ShotOutcome,
            Optional[CellState],
            List[Tuple[int, int]],
        ],
        None,
    ]:
        if self.player1 is None or self.player2 is None:
            raise RuntimeError

        await self.initialize()

        current_player = 0

        while self._is_game_running():
            if current_player == 0:
                shot = await self.player1.shoot(self.board2.get_masked_board())
                outcome, cell_state, changes = self.board2.shoot(shot)
            else:
                shot = await self.player2.shoot(self.board1.get_masked_board())
                outcome, cell_state, changes = self.board1.shoot(shot)

            yield current_player, shot, outcome, cell_state, changes

            current_player ^= 1
