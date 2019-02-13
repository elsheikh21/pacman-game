# How to get started

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

[Intro to Reinforcement learning](docs/RL_Intro.md)

[Intro to Markov Decision Process](docs/Markov_Decision_Process.md)

[Intro to Q Learning](docs/Q_Learning.md)

[Methods from Openai gym api](docs/about_openai_gym_methods.md)

---
