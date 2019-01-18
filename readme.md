# Pacman Game

## How to get started

1. Access the following directory
   - `C:\Users\<user name>\AppData\Local\Programs\Python\Python<version>\Lib`
2. make a new directory and name it `gym` (or whatever)
3. git clone https://github.com/openai/gym.git
4. cd gym
   - `current directory is C:\Users\<user name>\AppData\Local\Programs\Python\Python<version>\Lib\gym\gym`
5. `pip install -e .`
6. access `__init__.py` file in
   - `C:\Users\<username>\AppData\Local\Programs\Python\Python<version>\Lib\gym\gym\gym\envs`
7. Add to it the following code, save and exit

   ```
   register(
        id='MyPacman-v0',
        entry_point='gym.envs.classic_control:PacmanEnv',
        max_episode_steps=200,
        reward_threshold=4000,
   )
   ```

8. Access `classic_control` folder, and open the `__init__.py` file inside of it
9. Add to it the following line
   ```
   from gym.envs.classic_control.my_pacman import PacmanEnv
   ```
10. Add the following files to it,

    - `game_logic.py`
    - `pacman_game.py`
    - `my_pacman.py`

11. run `python -u pacman_game.py`

---

## Initialize the game

- Creating a 10X10 grid environment,
- Pacman starting position in the middle (approximately) {5, 4}.
- Environment made up of
  - Agent (pacman)
  - fixed walls,
  - fixed 4 ghosts are placed,
  - 2 special food pieces (power ups) lasts for 10 steps,
  - 66 food pieces, why? ((10 x 10) - 34) grid size subtract all other elements from it,
  - starting reward of 0,
  - utility functions of 0.

---

## Agent Actions

- Actions (Discrete 4):

  - Up(0) Agent will go up if possible, by adding 1 to rows
  - Down(1) Agent will go down if possible, by removing 1 from rows
  - Right(2) Agent will go right if possible, by adding 1 to cols
  - Left(3) Agent will go left if possible, by removing 1 from cols

- Action consequences

  - trying to go outside of the grid, by bumping into a wall
  - eating food (Regular food or special food)
  - nothing
  - Ghosts (PC not powered up, or, PC is powered up)

- Rewards (6):

  - reward = 0 -> Pacman is alive,
  - reward = -1000 -> Pacman is killed by a ghost,
  - reward = 10 -> Pacman eats a food piece,
  - reward = 50 -> Pacman eats a special
  - reward = 100 -> Pacman eats a ghost
  - reward = 1000 -> Pacman finished all food pieces.

---

## Rendering the game

- Map Values:

  - 0 food piece to eat
  - 1 ghosts
  - 2 walls
  - 3 eaten food piece
  - 9 Pacman
  - 11 special food piece

- Representation of the values
  - Food pieces to eat "F"
  - Special food "SF"
  - Ghosts "G"
  - Walls "X"
  - Eaten food pieces " "
  - Powered Up pacman "PC"
  - Normal pacman "pc"
