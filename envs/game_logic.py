import numpy as np
from gym import logger


def move_up_scenario(self):
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

            # If this is last episode then disable power up & reset counter
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


def move_down_scenario(self):
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


def move_right_scenario(self):
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


def move_left_scenario(self):
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
