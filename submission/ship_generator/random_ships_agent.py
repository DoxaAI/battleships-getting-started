from typing import List, Set, Tuple, Dict, Optional
import random

import numpy as np
from battleships import BaseAgent, ShotOutcome, Board, Ship, SETTINGS
from battleships.exceptions import ImpossibleShipGenerationException


def generate_ship_cells(
    start_coords: Tuple[int, int],
    size: int,
    board_dims: Tuple[int, int],
    free_cells: Set[Tuple[int, int]],
) -> Set[Tuple[int, int]]:
    ship_cells: Set[Tuple[int, int]] = set()
    unexplored_cells: Set[Tuple[int, int]] = set()

    if start_coords not in free_cells:
        raise ImpossibleShipGenerationException(
            f"Cannot generate ship with the following starting position {start_coords}"
        )

    unexplored_cells.add(start_coords)
    for _ in range(size):
        if not len(unexplored_cells):
            raise ImpossibleShipGenerationException(
                f"Cannot generate a ship of size {size} \
                in the following starting position {start_coords}"
            )
        cell_to_add = random.choice(list(unexplored_cells))
        unexplored_cells.remove(cell_to_add)
        ship_cells.add(cell_to_add)
        free_cells.remove(cell_to_add)

        possible_cells: List[Tuple[int, int]] = [
            (cell_to_add[0] - 1, cell_to_add[1]),
            (cell_to_add[0], cell_to_add[1] - 1),
            (cell_to_add[0], cell_to_add[1] + 1),
            (cell_to_add[0] + 1, cell_to_add[1]),
        ]
        for cell in possible_cells:
            if (
                cell[0] >= 0
                and cell[0] < board_dims[0]
                and cell[1] >= 0
                and cell[1] < board_dims[1]
                and cell in free_cells
            ):
                unexplored_cells.add(cell)

    return ship_cells


def _generate_ships(
    ship_specs: Dict[int, int], board_dims: Tuple[int, int]
) -> List[Set[Tuple[int, int]]]:
    board: Board = Board(board_dims)
    generated_ships: List[Set[Tuple[int, int]]] = []

    cells_to_populate: Set[Tuple[int, int]] = {
        (y, x) for y in range(10) for x in range(10)
    }
    ships_to_generate = [k for k, v in ship_specs.items() for _ in range(v)]

    for ship_size_to_generate in ships_to_generate:
        cells_left_to_test = cells_to_populate.copy()
        ship_cells: Optional[Set[Tuple[int, int]]] = None
        while ship_cells is None:
            if not len(cells_left_to_test):
                raise ImpossibleShipGenerationException(
                    f"Cannot realize given ships specification on a board of size {board_dims} \
                    or failed to realize it this time with random cell selection policy. \
                    If you're sure that it is possible to generate this configuration on the \
                    board run the algorithm again."
                )
            start_coords = random.choice(list(cells_left_to_test))
            cells_left_to_test.remove(start_coords)

            # try to generate a ship at the location, if failed continue with another starting cell
            try:
                ship_cells = generate_ship_cells(
                    start_coords,
                    ship_size_to_generate,
                    board_dims,
                    cells_to_populate.copy(),
                )
            except ImpossibleShipGenerationException:
                continue

        # try to create it and register on the board
        try:
            ship: Ship = Ship(ship_cells)
            board._register_ship(ship)
        except Exception as e:
            raise RuntimeError(str(e))

        # if all good, add the ship to a list of ships
        generated_ships.append(ship_cells)

        for y, x in ship_cells:
            # remove ship cells from cells_to_populate
            # print((y, x))
            if (y, x) in cells_to_populate:
                cells_to_populate.remove((y, x))

            # reserve all cells around the ship as well and remove them from cells_to_populate
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
                    or coord[0] >= board.size[0]
                    or coord[1] < 0
                    or coord[1] >= board.size[1]
                ):
                    continue

                if coord in cells_to_populate:
                    cells_to_populate.remove(coord)

    return generated_ships


def generate_ships(
    ship_specs: Dict[int, int], board_dims: Tuple[int, int]
) -> List[Set[Tuple[int, int]]]:
    for _ in range(10):
        try:
            generated_ships = _generate_ships(ship_specs, board_dims)
            return generated_ships
        except:
            continue
    raise ImpossibleShipGenerationException("Bad luck with generating ships.")
