# Getting Started with Battleships on DOXA
This repository contains everything you need to get started with Battleships on DOXA. For more information, check out the [competition page](https://doxaai.com/competition/battleships). 😎

Feel free to fork this repository and use it as the foundation for your own agents. You can also join the conversation on the [DOXA Community Discord server](https://discord.gg/MUvbQ3UYcf).

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
- `cli.py`: a CLI for running your Battleships agent against your input from keyboard (run with `python cli.py`)

## Battleship rules

For the sake of this competition, we use a 10x10 board and a traditional 1vs1 game flow. Initially, players decide on their ship configurations. Once this is done, they shoot by turns to an opponent's board. If a shot ends with a miss, the opponents continues, otherwise, if player hits opponent's ship, they get extra turn and can continue shooting. The game ends when a player looses all their ships. 

The game consists of two stages:
- ship placement - when players specify their ships positions
- shooting - when players shoot in turns to opponent's board

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

A shot is simply a pair of numbers - coordinates in the 2d grid. 

**NOTE: first coordinate is the row number (y coordinate in a 2d cartesian system), second coordinate is the column number (x coordinate in a 2d cartesian system).**

## Implementing an agent

First, clone this repository if you have not already done so. Then, you can start implementing your first agent by modifying the `Agent` class in `submission/agent.py`.

There are two mandatory methods in the `Agent` class that you have to implement:
- `get_ships()`
- `shoot(board)`

### `get_ships()` method
`get_ships()` should return a list of ships you want to place on your board. To be specific, each ship is represented as a `set` of `tuple`s of `int`s. Therefore, an example of a list of ships would be the following, representing 2 ships, a single-cell ship at (1, 2) and a double-cell ship with cells at (4, 5) and (4, 6):
```py
[{(1, 2)}, {(4, 5), (4, 6)}]
```

**NOTE:** Keep in mind that the list of return ships must match the specified number of shapes of ships described in the subsection *Ship count, shapes and configurations*.

### `shoot(board)` method

The `shoot(board)` method should return the desired shot location in the format (row, column) as a `tuple` of `int`s. An example of a valid shot on a 10x10 board:

```py
(1, 4)
```

The `shoot(board)` method gives you an additional information to determine your shooting strategy - the opponent's `board`. Board contains useful information about the state of the opponent's board. Each cell of the board has a CellState value.
```py
class CellState(IntEnum):
    EMPTY = 0
    HEALTHY = 1
    MISS = 2
    HIT = 3
    DESTROYED = 4
```

The `EMPTY` in the context of opponent's board means that the cell was not discovered before, `MISS` indicates that an agent already shot there but missed, `HIT` indicates a ship cell that was hit, however the whole ship was not completely destroyed (it may be worth shooting around!), and `DESTROYED` means that the cell is a part of an already destroyed ship.

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

Links worth exploring (keep in mind that their rules may slightly differ from our competition):

[https://towardsdatascience.com/coding-an-intelligent-battleship-agent-bf0064a4b319](https://towardsdatascience.com/coding-an-intelligent-battleship-agent-bf0064a4b319)

[https://cliambrown.com/battleship/](https://cliambrown.com/battleship/)

[https://datagenetics.com/blog/december32011/index.html](https://datagenetics.com/blog/december32011/index.html)

[https://pageperso.lis-lab.fr/guilherme.fonseca/battleship_conf.pdf](https://pageperso.lis-lab.fr/guilherme.fonseca/battleship_conf.pdf)


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
