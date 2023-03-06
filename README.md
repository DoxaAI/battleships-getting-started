# Getting Started with Battleships on DOXA

This repository contains everything you need to get started with Battleships on DOXA. For more information, check out the [competition page](https://doxaai.com/competition/battleships). 😎

Feel free to fork this repository and use it as the foundation for your own agents. You can also join the conversation on the [DOXA Community Discord server](https://discord.gg/MUvbQ3UYcf). 👀

## Prerequisites

Before you begin, please ensure that you have Python 3.9+ and the DOXA CLI installed.

If you do not yet have the DOXA CLI installed, you may do so using `pip`:

```bash
pip install -U doxa-cli
```

## Repository structure

- `submission/`: the directory that gets uploaded to DOXA
  - `submission/agent.py`: this is where you should implement your own agent!
  - `submission/doxa.yaml`: this is a configuration file used by DOXA to handle your submission
  - `submission/battleships/`: this is the Battleships engine 🚢
  - `submission/battleships/random_ship_generator.py`: module containing random ship generation code you may want to use (described below!)
- `examples/`: directory containing example agents
  - `examples/random_agent.py`: this is an implementation of a random agent
  - `examples/gaussian_agent.py`: this is an implementation of a gaussian random agent
  - `examples/random_ship_agent.py`: this is an implementation of the random agent above with randomly generated ships
- `cli.py`: a CLI for playing against your own Battleships agent (run with `python cli.py`)

## Battleship rules

For the sake of this competition, we use a 10 &times; 10 board and a traditional 1 vs. 1 game flow. Initially, players decide on their ship configurations. Once this is done, they take turns to make shots on their opponent's board. If a shot is a miss, the opponent continues with their move. Otherwise, if the player hits opponent's ship, they get extra turn and can continue shooting. The game ends when a player loses all their ships.

The game consists of two stages:
- ship placement - when players specify their ships positions
- shooting - when players take turns to make shots on their opponent's board

### Ship count, shapes and configurations

Each player should start with setting up their own ships. We use the following ship specification:
- 4 ships of 1 cell
- 3 ships of 2 cells
- 2 ships of 3 cells
- 1 ship of 4 cells

Ship cells can be arranged however player wants them to be arranged, although every two ship cells must share at least one edge.

Additionally, ships should be placed separately, such that they do not share edges or corners.

✅ Examples of 6 valid ships:

```
  0 1 2 3 4 5 6 7 8 9
0 - O - - - - - - - -
1 - - - - - - O O O -
2 - - - O - - - - - -
3 - - O O - - - - - -
4 - - - - - - - - - -
5 - - - - - O O O - -
6 - - - - - - O - - -
7 - O - - - - - - - -
8 - O - - - - - - O O
9 - - - - - - - - O O
```

❌ Examples of 3 invalid ships (all of them have at least one pair of cells, which do not share an edge):

```
  0 1 2 3 4 5 6 7 8 9
0 - - - - - - - - O -
1 - - - - - - O O - -
2 - - - O - - - - - -
3 - - O - - - - - - -
4 - - - - - - - - - -
5 - - - - - - - - - -
6 - - - - - - - - - -
7 - - - - - - - - O -
8 - - - - - - - - - O
9 - - - - - - - - O O
```

✅ Example of a valid configuration (all ships nicely spaced, no shared edges or corners):

```
  0 1 2 3 4 5 6 7 8 9
0 - - - - - - - - - O
1 - - - - - - - - - O
2 - - - O - - - O - O
3 O O - - - - - - - -
4 - - - - - - - - - -
5 O - O O O - O - - -
6 O - - - - - - - O -
7 - - - - - - - - O -
8 - - - - - - - - O O
9 - O - - O O - - - -
```

❌ Example of an invalid configuration (2 different ships sharing a corner):

```
  0 1 2 3 4 5 6 7 8 9
0 - - - - - - - - - -
1 - - - - - - - - - -
2 - - - - - - - - - -
3 - - O O O - - - - -
4 - - - - - O O - - -
5 - - - - - - O - - -
6 - - - - - - - - - -
7 - - - - - - - - - -
8 - - - - - - - - - -
9 - - - - - - - - - -
```

### Shooting

A shot is simply a pair of numbers - coordinates in the 2D grid.

**Note**: the first coordinate is the row number (`y` coordinate in a 2D cartesian system), second coordinate is the column number (`x` coordinate in a 2D cartesian system).

## Implementing an agent

First, clone this repository if you have not already done so. You can then start implementing your first agent by modifying the `Agent` class in `submission/agent.py`.

There are two mandatory methods in the `Agent` class that you have to implement:
- `get_ships()`
- `shoot(board)`

### `get_ships()` method

`get_ships()` should return a `list` of ships you want to place on your board. To be specific, each ship is represented as a `set` of `tuple`s of `int`s. An example of a list of ships would be the following, representing two ships, a single-cell ship at `(1, 2)` and a double-cell ship with cells at `(4, 5)` and `(4, 6)`:

```py
[{(1, 2)}, {(4, 5), (4, 6)}]
```

**Note**: keep in mind that the list of return ships must match the specified number of shapes of ships described in the subsection *Ship count, shapes and configurations*.

### `shoot(board)` method

The `shoot(board)` method should return the desired shot location in the format (row, column) as a `tuple` of `int`s. For example, a valid shot on a 10 &times; 10 board could be `(1, 4)`.

The `shoot(board)` method gives you an additional information to determine your shooting strategy - the opponent's `board`. The `Board` object contains useful information about the state of the opponent's board. Each cell of the board has a `CellState` value.

```py
class CellState(IntEnum):
    EMPTY = 0
    HEALTHY = 1
    MISS = 2
    HIT = 3
    DESTROYED = 4
```

The `EMPTY` in the context of opponent's board means that the cell was not discovered before. `MISS` indicates that an agent already shot there but missed. `HIT` indicates a ship cell has been hit, but it is part of a ship that has not been completely destroyed (it may be worth shooting around!). `DESTROYED` means that the cell is a part of an already destroyed ship.

### Optional `handle_outcome(shot, outcome)` method

After each shot, agent receives a shot outcome in the form of `handle_outcome(shot, outcome)` method. The `outcome` value is one of the following:
```py
class ShotOutcome(IntEnum):
    MISS = 0
    HIT = 1
    DESTROYED = 2
    REPEATED_SHOT = 3
    INVALID_SHOT = 4
```

This can be used to update agent's internal state if the agent has one!

By default, the agent registers the same ship configuration and shoots at random locations at the board. What interesting ship placement and shooting strategies can you come up with? 👀

## Examples

We give you three simple examples to help you get started:
- `examples/random_agent.py` implements an agent that initialises the same ship configuration every time it is run. It shoots uniformly at random cells on the opponent's board.
- `examples/gaussian_agent.py` is similar to the previous one, however it shoots more often in the central part of the board (or elsewhere if you play with the mean and variance of the gaussian distributions used!).
- `examples/random_ship_agent.py` is an interesting example, since each time it is run, it generates a different ship configuration using the `generate_ships()` method from `submission/ship_generator/random_ships_agent.py`. If you would like to use this method in your very own agent, just use the method - it's already imported for you!

Links worth exploring (keep in mind that their rules may slightly differ from our competition):
- [https://towardsdatascience.com/coding-an-intelligent-battleship-agent-bf0064a4b319](https://towardsdatascience.com/coding-an-intelligent-battleship-agent-bf0064a4b319)
- [https://cliambrown.com/battleship/](https://cliambrown.com/battleship/)
- [https://datagenetics.com/blog/december32011/index.html](https://web.archive.org/web/20221203125223/https://datagenetics.com/blog/december32011/index.html)
- [https://pageperso.lis-lab.fr/guilherme.fonseca/battleship_conf.pdf](https://pageperso.lis-lab.fr/guilherme.fonseca/battleship_conf.pdf)

## Running the game locally

You can play against your own agent manually via keyboard input using the local Python `cli.py` script.

The ship initialisation command has a specific format, and you always need to initialise all ships at once. Ships are separated by a single comma `,`. On the other hand, ship cell coordinates are separated by a space ` ` and are in (`y, x`) format.

Here is an example of a valid ship initialisation command (feel free to copy it!):
```
2 3,5 8,0 5,4 2,1 7 2 7,6 6 7 6,4 5 4 6,2 9 3 9 1 9,8 3 8 4 9 4,6 1 8 1 7 1 6 0
```

Here is an example of a valid shot: `2 3`.

You may want to run two versions of your agent to play against each other. This is fun to watch! You can do it by commenting the following line in `cli.py` `main()`:
```python
    # Play using keyboard against your agent
    await ui.run(Game(HumanAgent(), Agent()))
```

and uncommentig:
```python
    # Uncomment the following line to run a game between two different agents
    # await ui.run(Game(Agent(), Agent()))
```

Moreover, you may want to run two completely different agents against each other to compare their performance! You can do it by appropriately modifying one of the lines above and additionally importing your second agent.

## Submitting to DOXA

Before you can submit your agent to DOXA, you must first ensure that you are logged into the DOXA CLI. You can do so with the following command:

```bash
doxa login
```

You should also make sure that you are enrolled on the [Battlships competition page](https://doxaai.com/competition/battleships).

Then, when you are ready to submit your agent (contained within the `submission` directory) to DOXA, run the following command from the root of the repository:

```bash
doxa upload submission
```

Please ensure that the `submission` directory only contains the files you wish to upload to DOXA. If you have renamed your submission directory to something else, substitute `submission` for the new directory name.
