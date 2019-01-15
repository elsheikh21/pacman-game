# core modules
import random
import numpy as np

# 3rd party modules
import gym
import game_logic
from gym import spaces


class PacmanEnv(gym.Env):

    def __init__(self):
        '''
        Pacman init method, creating a 10X10 grid environment,
        Pacman will be referred to as PC -powered up- or pc
        starting position in the middle {5, 5}.

        I introduced fixed walls, and 4 other randomly placed
        walls, and 5 ghosts are placed randomly, 2 special food
        pieces (power ups) lasts for 10 steps, 40 food pieces,
        and starting reward, utility functions of 0 and 0.

        Rewards (6):
        - reward = 0       -> Pacman is alive,
        - reward = -1000   -> Pacman is killed by a ghost,
        - reward = 10      -> Pacman eats a food piece,
        - reward = 50     -> Pacman eats a special
        - reward = 100     -> Pacman eats a ghost
        - reward = 1000    -> Pacman finished all food pieces.

        Actions (Discrete 4):
            - 0   Up
            - 1   Right
            - 2   Down
            - 3   Left

        Map Values:
            - 0     food piece to eat
            - 1     ghosts
            - 2     walls
            - 3     eaten food piece
            - 9     Pacman
            - 11    Self food piece
        '''

        # Grid of pacman
        self.grid = np.zeros((9, 9))
        # Pacman's initial location
        start_row = np.int_(4)
        start_col = np.int_(4)
        self.state = np.array([start_row, start_col])
        self.pacman = 9

        # Fixed position for some walls
        for i in range(9):
            self.grid[0][i] = 1
            self.grid[8][i] = 1

        self.grid[1][0] = 1
        self.grid[1][8] = 1
        self.grid[7][0] = 1
        self.grid[7][8] = 1

        # Total food pieces pacman has to eat
        # (number of cells 9 * 9) - number of other elements
        # walls, pacman, special food, ghosts
        self.food_pieces = ((9 * 9) - 34)
        # Number of food pieces Pacman ate
        self.food_ate = 0
        # Number of ghosts
        self.ghosts = 5
        # Number of walls to be set random
        self.walls = 4
        # Number of special food
        self.special_food = 2
        # Special power from special food
        self.special_power = 0
        # duration of power (in steps)
        self.specialPowerDuration = 10
        # counter of special power
        self.specialPowerCounter = 0

        # Ghosts locations (randomly)
        for i in range(self.ghosts):
            raw_index = random.randint(1, 7)
            col_index = random.randint(0, 8)

            if (self.grid[raw_index][col_index] == 0 and
                    (raw_index != 4 and col_index != 4)):
                self.grid[raw_index][col_index] = 1

        # Wall locations (randomly)
        for i in range(self.walls):
            raw_index = random.randint(1, 7)
            col_index = random.randint(0, 8)
            if (self.grid[raw_index][col_index] == 0 and
                    (raw_index != 4 and col_index != 4)):
                self.grid[raw_index][col_index] = 2

        # Reward {Check method documentation}
        self.reward = 0
        # Utility function
        self.utility = 0

        # Number of actions (up, right, bottom, left)
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        '''
        Up(0)      The agent will go up if possible, by adding 1 to rows
        Down(1)    The agent will go down if possible, by removing 1 to rows
        Right(2)   The agent will go right if possible, by adding 1 to rows
        Left(3)    The agent will go left if possible, by removing 1 to rows

        For every action, we will encounter one of several events
        1. trying to go outside of the grid
        2. eating a piece of food
        3. nothing
        4a. Ghost, PC not powered up
        4b. Ghost, PC is powered up
        '''

        # PC Moving upwards
        if(action == 0):
            game_logic.move_up_scenario(self)

        # PC Moving downwards
        elif(action == 1):
            game_logic.move_down_scenario(self)

        # PC turning Right
        elif(action == 2):
            game_logic.move_right_scenario(self)

        # PC turning Left
        else:
            game_logic.move_left_scenario(self)

        current_row = self.state[0]
        current_col = self.state[1]
        if (self.food_pieces == 0):
            reward = 1000
            game_over = True
            self.state[current_row][current_col]

        return np.array(self.state), reward, game_over, self.grid

    def render(self, mode='human'):
        counter = 0
        word = ''
        for row in self.grid:
            for cell in row:
                # Food pieces to eat
                if(cell == 0):
                    word = "•"
                # Special food
                elif(cell == 11):
                    word = "@"
                # Ghost location
                elif(cell == 1):
                    word = "†"
                # If the cell is a wall
                elif(cell == 2):
                    word = "X"
                # eaten food piece
                elif(cell == 3):
                    word = " "
                # Pacman
                elif(cell == 9):
                    if(self.specialPower == 1):
                        word = "PC"
                    else:
                        word = "pc"

                print(word, end=" | ")
                counter += 1
                if(counter == 10):
                    counter = 0
                    print("\r")

    def reset(self):
        self.state = np.array([4, 4])
        return np.array(self.state)

    def getGrid(self):
        return self.grid
