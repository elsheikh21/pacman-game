import gym
from gym import spaces

import numpy as np

from game_logic import (legal_actions_set, move_down_scenario,
                        move_left_scenario, move_right_scenario,
                        move_up_scenario)
from game_logic import map_states, get_state_mapping


class PacmanEnv(gym.Env):

    def __init__(self):
        '''
        Pacman init method, creating a 10X10 grid environment,
        Pacman will be referred to as PC -powered up- or pc
        starting position in the middle {5, 5}.

        I introduced fixed walls, and 4 other randomly placed
        walls, and 5 ghosts are placed randomly, 2 special food
        pieces (power ups) lasts for 10 steps, 40 food pieces,
        and starting reward functions of 0 and 0.

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
            - 11    special food piece
        '''

        # Grid of pacman
        self.grid = np.zeros((10, 10))
        # Pacman's initial location
        start_row, start_col = np.int_(5), np.int_(4)
        self.state = np.array([start_row, start_col])
        self.pacman = 9

        # Fixed position for some walls
        for i in range(10):
            self.grid[0][i] = 2
            self.grid[9][i] = 2
        for j in range(10):
            self.grid[j][0] = 2
            self.grid[j][9] = 2

        # Total food pieces pacman has to eat
        # (number of cells 9 * 9) - number of other elements
        # walls, pacman, special food, ghosts
        self.food_pieces = ((10 * 10) - 34)
        # Number of food pieces Pacman ate
        self.food_ate = 0
        # Number of ghosts
        self.ghosts = 4
        # Number of walls to be set random
        # self.walls = 4
        # Number of special food
        self.special_food = 2
        # Special power from special food
        self.special_power = 0
        # duration of power (in steps)
        self.special_power_duration = 10
        # counter of special power
        self.special_power_counter = 0

        # Ghosts locations
        self.grid[2][8] = 1
        self.grid[8][2] = 1
        self.grid[1][4] = 1
        self.grid[4][1] = 1

        # Special food locations
        self.grid[1][1] = 11
        self.grid[8][8] = 11

        # Reward
        self.reward = 0
        # Utility function
        # self.utility = 0

        # Number of actions (up, right, bottom, left)
        self.action_space = spaces.Discrete(4)
        # Number of observations/states = no of possible/legal states ()
        # multiplied by the no of actions (4)
        # 10x10(all possible locations) - 36 (wall locations)
        # 64 possible states
        walls_number = np.array2string(self.grid).count('2')
        legal_states = (10 * 10) - walls_number
        self.observation_space = spaces.Discrete(legal_states)

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


        Rewards (6):
        - reward = -1000   -> Pacman is killed by a ghost,
        - reward = 0       -> Pacman is alive,
        - reward = 10      -> Pacman eats a food piece,
        - reward = 50     -> Pacman eats a special
        - reward = 100     -> Pacman eats a ghost
        - reward = 1000    -> Pacman finished all food pieces.

        '''
        legal_actions_set(self)
        # Penalty for every step the agent makes
        # PC Moving upwards
        reward = 0
        if(action == 0):
            return move_up_scenario(self, reward)
        # PC Moving downwards
        elif(action == 1):
            return move_down_scenario(self, reward)
        # PC turning Right
        elif(action == 2):
            return move_right_scenario(self, reward)
        # PC turning Left
        else:
            return move_left_scenario(self, reward)

    def render(self, mode='human'):
        '''
        Map Values:
            - 0     food piece to eat
            - 1     ghosts
            - 2     walls
            - 3     eaten food piece
            - 9     Pacman
            - 11    special food piece
        '''

        grid = self.grid
        grid_str = np.array2string(grid).replace('0', "F   ").replace(
            '11',  "SF   ").replace('1', "G   ").replace(
                '3', "    ").replace('2', "X   ")
        if(self.special_power == 1):
            grid_str = grid_str.replace('9', 'PC  ')
        else:
            grid_str = grid_str.replace('9', 'pc  ')
        print(grid_str)

    def reset(self):
        '''
        Just invokes a new instance of the game
        '''
        self.__init__()
        states_list = map_states()
        state_idx = get_state_mapping(self.state, states_list)
        return state_idx
