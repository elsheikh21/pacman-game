# core modules
import random
import numpy as np

# 3rd party modules
import gym
from gym import spaces, logger


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
            - 11    special food piece
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
            self.grid[0][i] = 2
            self.grid[8][i] = 2

        self.grid[1][0] = 2
        self.grid[1][8] = 2
        self.grid[7][0] = 2
        self.grid[7][8] = 2

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

        # Special food locations (randomly)
        for i in range(self.special_food):
            raw_index = random.randint(1, 7)
            col_index = random.randint(0, 8)
            if (self.grid[raw_index][col_index] == 0 and
                    (raw_index != 4 and col_index != 4)):
                self.grid[raw_index][col_index] = 11

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
        reward = 0
        # PC Moving upwards
        if(action == 0):
            current_row = self.state[0]
            current_col = self.state[1]
            grid_now = self.grid[current_row-1][current_col]
            logger.info('PC moving upwards')
            # PC is fed up, and wants to commit suicide
            if(current_row - 1 < 0):
                logger.warn('Cannot move out of the grid.')
                self.state = np.array([current_row, current_col])
                reward = 0
                game_over = False
                return np.array([self.state]), reward, game_over, self.grid
            # PC is running into a food piece to eat
            elif(grid_now == 0):
                logger.info('PC is less hungry now')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Since we moved up, we decrement our rows count
                current_row -= 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 10 points for eating the food piece
                reward = 10
                # Game is not over yet
                game_over = False
                self.food_pieces -= 1
                self.food_ate += 1
            # There is a wall
            elif(grid_now == 2):
                logger.warn('Bumping PC\'s head to the wall, won\'t help it.')
                # No updates to the state of course nor the grid,
                # nor reward, nor game ended
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
            # There is a ghost
            elif(grid_now == 1):
                # First scenario, that PC is powered up
                if(self.special_power == 1):
                    # Increment its counter, to maintain the ability's duration
                    self.specialPowerCounter += 1
                    # if PC is still powered up
                    if(self.specialPowerCounter > self.specialPowerDuration):
                        logger.info('PC reduced number of ghosts by 1...')
                        # Since we moved up, we decrement our rows count
                        current_row -= 1
                        self.state = [current_row, current_col]
                        # Update the grid with the new pacman position
                        self.grid[current_row, current_col] = self.pacman
                        # Update number of ghosts, reduce them by one
                        self.ghosts -= 1
                        # Update reward with 100 points for eating a ghost
                        reward = 100
                        # Game is not over yet
                        game_over = False

                    # If last episode then disable power up & reset counter
                    else:
                        self.special_power = 0
                        self.specialPowerCounter = 0

                # Second scenario, poor PC is not powered UP,
                # RIP Mr. Pacman
                else:
                    logger.error('poor pacman died :(, GAME OVER')
                    # No need to update the state or the grid
                    # self.state = [current_row, current_col]
                    # self.grid[current_row, current_col] = self.pacman
                    reward = -1000
                    game_over = True
            # There is a powering up food piece
            elif(grid_now == 11):
                logger.info('PC IS JACKED UP NOW')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Make PC powered up
                self.special_power = 1
                # Since we moved up, we decrement our rows count
                current_row -= 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 50 points for eating the special food
                reward = 50
                # Game is not over yet
                game_over = False
                self.special_food -= 1
                self.food_ate += 1
            # There is nothing he bumps into
            else:
                # Just update pacman's position and grid
                # Yet game ain't over yet
                current_row -= 1
                self.state = [current_row, current_col]
                self.grid[current_row][current_col] = self.pacman
                reward = 0
                game_over = False

        # PC Moving downwards
        elif(action == 1):
            current_row = self.state[0]
            current_col = self.state[1]
            grid_now = self.grid[current_row+1][current_col]
            logger.info('PC moving downwards')
            # PC is fed up, and wants to commit suicide
            if(current_row + 1 > 8):
                logger.warn('Cannot move out of the grid.')
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
                return np.array([self.state]), reward, game_over, self.grid
            # PC is running into a food piece to eat
            elif(grid_now == 0):
                logger.info('PC is less hungry now')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Since we moved up, we decrement our rows count
                current_row += 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 10 points for eating the food piece
                reward = 10
                # Game is not over yet
                game_over = False
                self.food_pieces -= 1
                self.food_ate += 1
            # There is a wall
            elif(grid_now == 2):
                logger.warn('Bumping PC\'s head to the wall, won\'t help it.')
                # No updates to the state of course nor the grid,
                # nor reward, nor game ended
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
            # There is a ghost
            elif(grid_now == 1):
                # First scenario, that PC is powered up
                if(self.special_power == 1):
                    # Increment its counter, to maintain the ability's duration
                    self.specialPowerCounter += 1
                    # if PC is still powered up
                    if(self.specialPowerCounter > self.specialPowerDuration):
                        logger.info('PC reduced number of ghosts by 1...')
                        # Since we moved up, we decrement our rows count
                        current_row += 1
                        self.state = [current_row, current_col]
                        # Update the grid with the new pacman position
                        self.grid[current_row, current_col] = self.pacman
                        # Update number of ghosts, reduce them by one
                        self.ghosts -= 1
                        # Update reward with 100 points for eating a ghost
                        reward = 100
                        # Game is not over yet
                        game_over = False

                    # If last episode then disable power up and reset counter
                    else:
                        self.special_power = 0
                        self.specialPowerCounter = 0

                # Second scenario, poor PC is not powered UP,
                # RIP Mr. Pacman
                else:
                    logger.error('poor pacman died :(, GAME OVER')
                    # No need to update the state or the grid
                    # self.state = [current_row, current_col]
                    # self.grid[current_row, current_col] = self.pacman
                    reward = -1000
                    game_over = True
            # There is a powering up food piece
            elif(grid_now == 11):
                logger.info('PC IS JACKED UP NOW')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Make PC powered up
                self.special_power = 1
                # Since we moved up, we decrement our rows count
                current_row += 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 50 points for eating the special food
                reward = 50
                # Game is not over yet
                game_over = False
                self.special_food -= 1
                self.food_ate += 1
            # There is nothing he bumps into
            else:
                # Just update pacman's position and grid
                # Yet game ain't over yet
                current_row += 1
                self.state = [current_row, current_col]
                self.grid[current_row][current_col] = self.pacman
                reward = 0
                game_over = False

        # PC turning Right
        elif(action == 2):
            current_row = self.state[0]
            current_col = self.state[1]
            grid_now = self.grid[current_row][current_col+1]
            logger.info('PC moving downwards')
            # PC is fed up, and wants to commit suicide
            if(current_row + 1 > 8):
                logger.warn('Cannot move out of the grid.')
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
                return np.array([self.state]), reward, game_over, self.grid
            # PC is running into a food piece to eat
            elif(grid_now == 0):
                logger.info('PC is less hungry now')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Since we moved up, we decrement our rows count
                current_col += 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 10 points for eating the food piece
                reward = 10
                # Game is not over yet
                game_over = False
                self.food_pieces -= 1
                self.food_ate += 1
            # There is a wall
            elif(grid_now == 2):
                logger.warn(
                    'Bumping PC\'s head to the wall, won\'t help it.')
                # No updates to the state of course nor the grid,
                # nor reward, nor game ended
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
            # There is a ghost
            elif(grid_now == 1):
                # First scenario, that PC is powered up
                if(self.special_power == 1):
                    # Increment its counter, to maintain the ability's duration
                    self.specialPowerCounter += 1
                    # if PC is still powered up
                    if(self.specialPowerCounter > self.specialPowerDuration):
                        logger.info('PC reduced number of ghosts by 1...')
                        # Since we moved up, we decrement our rows count
                        current_col += 1
                        self.state = [current_row, current_col]
                        # Update the grid with the new pacman position
                        self.grid[current_row, current_col] = self.pacman
                        # Update number of ghosts, reduce them by one
                        self.ghosts -= 1
                        # Update reward with 100 points for eating a ghost
                        reward = 100
                        # Game is not over yet
                        game_over = False

                    # If last episode then disable power up and reset counter
                    else:
                        self.special_power = 0
                        self.specialPowerCounter = 0

                # Second scenario, poor PC is not powered UP,
                # RIP Mr. Pacman
                else:
                    logger.error('poor pacman died :(, GAME OVER')
                    # No need to update the state or the grid
                    # self.state = [current_row, current_col]
                    # self.grid[current_row, current_col] = self.pacman
                    reward = -1000
                    game_over = True
            # There is a powering up food piece
            elif(grid_now == 11):
                logger.info('PC IS JACKED UP NOW')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Make PC powered up
                self.special_power = 1
                # Since we moved up, we decrement our rows count
                current_col += 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 50 points for eating the special food
                reward = 50
                # Game is not over yet
                game_over = False
                self.special_food -= 1
                self.food_ate += 1
            # There is nothing he bumps into
            else:
                # Just update pacman's position and grid
                # Yet game ain't over yet
                current_col += 1
                self.state = [current_row, current_col]
                self.grid[current_row][current_col] = self.pacman
                reward = 0
                game_over = False

        # PC turning Left
        else:
            current_row = self.state[0]
            current_col = self.state[1]
            grid_now = self.grid[current_row][current_col-1]
            logger.info('PC moving downwards')
            # PC is fed up, and wants to commit suicide
            if(current_row - 1 < 0):
                logger.warn('Cannot move out of the grid.')
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
                return np.array([self.state]), reward, game_over, self.grid
            # PC is running into a food piece to eat
            elif(grid_now == 0):
                logger.info('PC is less hungry now')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Since we moved up, we decrement our rows count
                current_col -= 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 10 points for eating the food piece
                reward = 10
                # Game is not over yet
                game_over = False
                self.food_pieces -= 1
                self.food_ate += 1
            # There is a wall
            elif(grid_now == 2):
                logger.warn('Bumping PC\'s head to the wall, won\'t help it.')
                # No updates to the state of course nor the grid,
                # nor reward, nor game ended
                self.state = [current_row, current_col]
                reward = 0
                game_over = False
            # There is a ghost
            elif(grid_now == 1):
                # First scenario, that PC is powered up
                if(self.special_power == 1):
                        # Increment its counter, to maintain the ability's duration
                    self.specialPowerCounter += 1
                    # if PC is still powered up
                    if(self.specialPowerCounter > self.specialPowerDuration):
                        logger.info('PC reduced number of ghosts by 1...')
                        # Since we moved up, we decrement our rows count
                        current_col -= 1
                        self.state = [current_row, current_col]
                        # Update the grid with the new pacman position
                        self.grid[current_row, current_col] = self.pacman
                        # Update number of ghosts, reduce them by one
                        self.ghosts -= 1
                        # Update reward with 100 points for eating a ghost
                        reward = 100
                        # Game is not over yet
                        game_over = False

                    # If last episode then disable power up and reset counter
                    else:
                        self.special_power = 0
                        self.specialPowerCounter = 0

                # Second scenario, poor PC is not powered UP,
                # RIP Mr. Pacman
                else:
                    logger.error('poor pacman died :(, GAME OVER')
                    # No need to update the state or the grid
                    # self.state = [current_row, current_col]
                    # self.grid[current_row, current_col] = self.pacman
                    reward = -1000
                    game_over = True
            # There is a powering up food piece
            elif(grid_now == 11):
                logger.info('PC IS JACKED UP NOW')
                # PC ate the food piece, replace it with an empty piece
                grid_now = 3
                # Make PC powered up
                self.special_power = 1
                # Since we moved up, we decrement our rows count
                current_col -= 1
                self.state = [current_row, current_col]
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update reward with 50 points for eating the special food
                reward = 50
                # Game is not over yet
                game_over = False
                self.special_food -= 1
                self.food_ate += 1
            # There is nothing he bumps into
            else:
                # Just update pacman's position and grid
                # Yet game ain't over yet
                current_col -= 1
                self.state = [current_row, current_col]
                self.grid[current_row][current_col] = self.pacman
                reward = 0
                game_over = False

        current_row = self.state[0]
        current_col = self.state[1]
        if (self.food_pieces == 0):
            reward = 1000
            game_over = True
            self.state[current_row][current_col]

        return np.array(self.state), reward, game_over, self.grid

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
        grid_world = str("")
        for i in range(9):
            grid_world += "[  "
            for k in range(9):
                # food
                if (grid[i][k] == 0):
                    grid_world += ".   "
                # Special food
                elif (grid[i][k] == 11):
                    grid_world += "0   "
                # Ghost
                elif (grid[i][k] == 1):
                    grid_world += "G   "
                # pacman
                elif (grid[i][k] == 9):
                    if(self.special_power == 1):
                        grid_world += "PC  "
                    else:
                        grid_world += "pc  "
                # Food eaten
                elif (grid[i][k] == 3):
                    grid_world += "   "
                # Wall
                else:
                    grid_world += "X   "

            grid_world += "]" + '\n'
        print(grid_world)
        # counter = 0
        # word = ''
        # for row in self.grid:
        #     for cell in row:
        #         # Food pieces to eat
        #         if(cell == 0):
        #             word = "F"
        #         # Special food
        #         elif(cell == 11):
        #             word = "SF"
        #         # Ghost location
        #         elif(cell == 1):
        #             word = "G"
        #         # If the cell is a wall
        #         elif(cell == 2):
        #             word = "X"
        #         # eaten food piece
        #         elif(cell == 3):
        #             word = " "
        #         # Pacman
        #         elif(cell == 9):
        #             if(self.special_power == 1):
        #                 word = "PC"
        #             else:
        #                 word = "pc"

        #         print(word, end=" | ")
        #         counter += 1
        #         if(counter == 10):
        #             counter = 0
        #             print("\r")

    def reset(self):
        self.state = np.array([4, 4])
        return np.array(self.state)

    def getGrid(self):
        return self.grid
