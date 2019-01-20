import numpy as np


def legal_actions_set(self):
    current_row = self.state[0]
    current_col = self.state[1]
    legal_actions = ['up', 'right', 'down', 'left']
    if(self.grid[current_row-1][current_col] == 2):
        legal_actions.remove('up')
    if(self.grid[current_row][current_col+1] == 2):
        legal_actions.remove('right')
    if(self.grid[current_row+1][current_col] == 2):
        legal_actions.remove('down')
    if(self.grid[current_row][current_col-1] == 2):
        legal_actions.remove('left')

    current_state = np.array([current_row, current_col])
    actions = " ".join(str(action) for action in legal_actions)
    print('In this state {}, set of possible actions are {}'.format(
        current_state, actions))


def special_power_scenario(self):
    if(self.special_power == 1):
        self.special_power_counter += 1
        if(self.special_power_counter > self.special_power_duration):
            self.special_power = 0
            self.special_power_duration = 0


def move_up_scenario(self, reward):
    game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    grid_now = self.grid[current_row-1][current_col]
    print('Action: agent moving upwards')
    # PC is fed up, and wants to commit suicide
    if(current_row - 1 < 0):
        special_power_scenario(self)
        # print('Cannot move out of the grid.')
        self.state = np.array([current_row, current_col])
        reward += 0
        game_over = False
    # PC is running into a food piece to eat
    elif(grid_now == 0):
        special_power_scenario(self)
        print('[INFO] agent ate food piece.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Since we moved up, we decrement our rows count
        current_row -= 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row+1, current_col] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 10 points for eating the food piece
        reward += 10
        # Game is not over yet
        game_over = False
        self.food_pieces -= 1
        self.food_ate += 1
    # There is a wall
    elif(grid_now == 2):
        special_power_scenario(self)
        print('[INFO] Bumping into the wall.')
        # No updates to the state of course nor the grid,
        # nor reward, nor game ended
        self.state = [current_row, current_col]
        reward += -5
        game_over = False
    # There is a ghost
    elif(grid_now == 1):
        # First scenario, that PC is powered up
        if(self.special_power == 1):
            # Increment its counter, to maintain the ability's duration
            self.special_power_counter += 1
            # if PC is still powered up
            if(self.special_power_counter > self.special_power_duration):
                print('[INFO] agent killed a ghost.')
                # Since we moved up, we decrement our rows count
                current_row -= 1
                self.state = [current_row, current_col]
                # Update the grid with remove old pacman position
                self.grid[current_row+1, current_col] = float(3.0)
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update number of ghosts, reduce them by one
                self.ghosts -= 1
                # Update reward with 100 points for eating a ghost
                reward += 100
                # Game is not over yet
                game_over = False

            # If this is last episode then disable power up & reset counter
            else:
                self.special_power = 0
                self.special_power_counter = 0

        # Second scenario, poor PC is not powered UP,
        # RIP Mr. Pacman
        else:
            print('[GAME OVER] Agent died. \n')
            # No need to update the state or the grid
            self.grid[current_row, current_col+1] = float(3.0)
            reward -= 1000
            game_over = True
    # There is a powering up food piece
    elif(grid_now == 11):
        special_power_scenario(self)
        print('[INFO] agent is on steroids.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Make PC powered up
        self.special_power = 1
        # Since we moved up, we decrement our rows count
        current_row -= 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row+1, current_col] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 50 points for eating the special food
        reward += 50
        # Game is not over yet
        game_over = False
        self.special_food -= 1
        self.food_ate += 1
    # There is nothing he bumps into
    else:
        special_power_scenario(self)
        # Just update pacman's position and grid
        # Yet game ain't over yet
        current_row -= 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row+1, current_col] = float(3.0)
        self.grid[current_row][current_col] = self.pacman
        reward += 0
        game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    if (self.food_pieces == 0):
        reward += 1000
        game_over = True
        self.state[current_row][current_col]
    return np.array([self.state]), reward, game_over, self.grid


def move_down_scenario(self, reward):
    game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    grid_now = self.grid[current_row+1][current_col]
    print('Action: agent moving downwards')
    # PC is fed up, and wants to commit suicide
    if(current_row + 1 > 9):
        special_power_scenario(self)
        # print('Cannot move out of the grid.')
        self.state = [current_row, current_col]
        reward += 0
        game_over = False
    # PC is running into a food piece to eat
    elif(grid_now == 0):
        special_power_scenario(self)
        print('[INFO] agent ate food piece.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Since we moved up, we decrement our rows count
        current_row += 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row-1, current_col] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 10 points for eating the food piece
        reward += 10
        # Game is not over yet
        game_over = False
        self.food_pieces -= 1
        self.food_ate += 1
    # There is a wall
    elif(grid_now == 2):
        special_power_scenario(self)
        print('[INFO] Bumping into the wall.')
        # No updates to the state of course nor the grid,
        # nor reward, nor game ended
        self.state = [current_row, current_col]
        reward += -5
        game_over = False
    # There is a ghost
    elif(grid_now == 1):
        # First scenario, that PC is powered up
        if(self.special_power == 1):
            # Increment its counter, to maintain the ability's duration
            self.special_power_counter += 1
            # if PC is still powered up
            if(self.special_power_counter > self.special_power_duration):
                print('[INFO] agent killed a ghost.')
                # Since we moved up, we decrement our rows count
                current_row += 1
                self.state = [current_row, current_col]
                # Update the grid with remove old pacman position
                self.grid[current_row-1, current_col] = float(3.0)
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update number of ghosts, reduce them by one
                self.ghosts -= 1
                # Update reward with 100 points for eating a ghost
                reward += 100
                # Game is not over yet
                game_over = False

            # If last episode then disable power up and reset counter
            else:
                self.special_power = 0
                self.special_power_counter = 0

        # Second scenario, poor PC is not powered UP,
        # RIP Mr. Pacman
        else:
            print('[GAME OVER] Agent died \n')
            # No need to update the state or the grid
            self.grid[current_row, current_col+1] = float(3.0)
            reward -= 1000
            game_over = True
    # There is a powering up food piece
    elif(grid_now == 11):
        special_power_scenario(self)
        print('[INFO] agent is on steroids.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Make PC powered up
        self.special_power = 1
        # Since we moved up, we decrement our rows count
        current_row += 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row-1, current_col] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 50 points for eating the special food
        reward += 50
        # Game is not over yet
        game_over = False
        self.special_food -= 1
        self.food_ate += 1
    # There is nothing he bumps into
    else:
        special_power_scenario(self)
        # Just update pacman's position and grid
        # Yet game ain't over yet
        current_row += 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row-1, current_col] = float(3.0)
        self.grid[current_row][current_col] = self.pacman
        reward += 0
        game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    if (self.food_pieces == 0):
        reward += 1000
        game_over = True
        self.state[current_row][current_col]
    return np.array([self.state]), reward, game_over, self.grid


def move_right_scenario(self, reward):
    game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    grid_now = self.grid[current_row][current_col+1]
    print('Action: agent moving right')
    # PC is fed up, and wants to commit suicide
    if(current_col + 1 > 9):
        special_power_scenario(self)
        # print('Cannot move out of the grid.')
        self.state = [current_row, current_col]
        reward += 0
        game_over = False

    # PC is running into a food piece to eat
    elif(grid_now == 0):
        special_power_scenario(self)
        print('[INFO] agent ate food piece.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Since we moved up, we decrement our rows count
        current_col += 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row, current_col-1] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 10 points for eating the food piece
        reward += 10
        # Game is not over yet
        game_over = False
        self.food_pieces -= 1
        self.food_ate += 1

    # There is a wall
    elif(grid_now == 2):
        special_power_scenario(self)
        print('[INFO] Bumping into the wall.')
        # No updates to the state of course nor the grid,
        # nor reward, nor game ended
        self.state = [current_row, current_col]
        reward += -5
        game_over = False

    # There is a ghost
    elif(grid_now == 1):
        # First scenario, that PC is powered up
        if(self.special_power == 1):
            # Increment its counter, to maintain the ability's duration
            self.special_power_counter += 1
            # if PC is still powered up
            if(self.special_power_counter > self.special_power_duration):
                print('[INFO] agent killed a ghost.')
                # Since we moved up, we decrement our rows count
                current_col += 1
                self.state = [current_row, current_col]
                # Update the grid with remove old pacman position
                self.grid[current_row, current_col-1] = float(3.0)
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update number of ghosts, reduce them by one
                self.ghosts -= 1
                # Update reward with 100 points for eating a ghost
                reward += 100
                # Game is not over yet
                game_over = False

            # If last episode then disable power up and reset counter
            else:
                self.special_power = 0
                self.special_power_counter = 0

        # Second scenario, poor PC is not powered UP,
        # RIP Mr. Pacman
        else:
            print('[GAME OVER] Agent died \n')
            # No need to update the state or the grid
            self.grid[current_row, current_col+1] = float(3.0)
            reward -= 1000
            game_over = True
    # There is a powering up food piece
    elif(grid_now == 11):
        special_power_scenario(self)
        print('[INFO] agent is on steroids.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Make PC powered up
        self.special_power = 1
        # Since we moved up, we decrement our rows count
        current_col += 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row, current_col-1] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 50 points for eating the special food
        reward += 50
        # Game is not over yet
        game_over = False
        self.special_food -= 1
        self.food_ate += 1

    # There is nothing he bumps into
    else:
        special_power_scenario(self)
        # Just update pacman's position and grid
        # Yet game ain't over yet
        current_col += 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row, current_col-1] = float(3.0)
        self.grid[current_row][current_col] = self.pacman
        reward += 0
        game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    if (self.food_pieces == 0):
        reward += 1000
        game_over = True
        self.state[current_row][current_col]
    return np.array([self.state]), reward, game_over, self.grid


def move_left_scenario(self, reward):
    game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    grid_now = self.grid[current_row][current_col-1]
    print('Action: agent moving left')
    # PC is fed up, and wants to commit suicide
    if(current_col - 1 < 0):
        special_power_scenario(self)
        # print('Cannot move out of the grid.')
        self.state = [current_row, current_col]
        reward += 0
        game_over = False

    # PC is running into a food piece to eat
    elif(grid_now == 0):
        special_power_scenario(self)
        print('[INFO] agent ate food piece.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Since we moved up, we decrement our rows count
        current_col -= 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row, current_col+1] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 10 points for eating the food piece
        reward += 10
        # Game is not over yet
        game_over = False
        self.food_pieces -= 1
        self.food_ate += 1

    # There is a wall
    elif(grid_now == 2):
        special_power_scenario(self)
        print('[INFO] Bumping into the wall.')
        # No updates to the state of course nor the grid,
        # nor reward, nor game ended
        self.state = [current_row, current_col]
        reward += -5
        game_over = False

    # There is a ghost
    elif(grid_now == 1):
        # First scenario, that PC is powered up
        if(self.special_power == 1):
            # Increment counter, maintaining ability duration
            self.special_power_counter += 1
            # if PC is still powered up
            if(self.special_power_counter > self.special_power_duration):
                print('[INFO] agent is on steroids.')
                # Since we moved up, we decrement our rows count
                current_col -= 1
                self.state = [current_row, current_col]
                # Update the grid with remove old pacman position
                self.grid[current_row, current_col+1] = float(3.0)
                # Update the grid with the new pacman position
                self.grid[current_row, current_col] = self.pacman
                # Update number of ghosts, reduce them by one
                self.ghosts -= 1
                # Update reward with 100 points for eating a ghost
                reward += 100
                # Game is not over yet
                game_over = False

            # If last episode then disable power up and reset counter
            else:
                self.special_power = 0
                self.special_power_counter = 0

        # Second scenario, poor PC is not powered UP,
        # RIP Mr. Pacman
        else:
            print('[GAME OVER] Agent died \n')
            # No need to update the state or the grid
            # Update the grid with remove old pacman position
            self.grid[current_row, current_col+1] = float(3.0)
            reward -= 1000
            game_over = True

    # There is a powering up food piece
    elif(grid_now == 11):
        special_power_scenario(self)
        print('[INFO] agent is on steroids.')
        # PC ate the food piece, replace it with an empty piece
        grid_now = 3
        # Make PC powered up
        self.special_power = 1
        # Since we moved up, we decrement our rows count
        current_col -= 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row, current_col+1] = float(3.0)
        # Update the grid with the new pacman position
        self.grid[current_row, current_col] = self.pacman
        # Update reward with 50 points for eating the special food
        reward += 50
        # Game is not over yet
        game_over = False
        self.special_food -= 1
        self.food_ate += 1

    # There is nothing he bumps into
    else:
        special_power_scenario(self)
        # Just update pacman's position and grid
        # Yet game ain't over yet
        current_col -= 1
        self.state = [current_row, current_col]
        # Update the grid with remove old pacman position
        self.grid[current_row, current_col+1] = float(3.0)
        self.grid[current_row][current_col] = self.pacman
        reward += 0
        game_over = False
    current_row = self.state[0]
    current_col = self.state[1]
    if (self.food_pieces == 0):
        reward += 1000
        game_over = True
        self.state[current_row][current_col]
    return np.array([self.state]), reward, game_over, self.grid
