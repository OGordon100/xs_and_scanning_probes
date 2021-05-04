import warnings

from nOmicron.microscope import IO, xy_scanner, black_box
from typing import Tuple

from nOmicron.utils.plotting import nanomap

from model.self_play_test import SelfPlayTester
from shapes.shapes import DataShape
from matplotlib import pyplot as plt
import numpy as np


class STMTicTacToe:
    def __init__(self, scan_bias, scan_setpoint, passivate_setpoint,
                 player_1_type="human", player_2_type="best", first_player="player_1", render_mode="plot"):
        """Play noughts and crosses in STM using RL

        Parameters
        ----------
        scan_bias: float
            Scan voltage bias (Volts)
        scan_setpoint: float
            Scan sepoint current (Amps)
        passivate_setpoint: float
            Setpoint current to use during passivation (Amps)
        player_1_type: str
            Player 1. One of 'best', 'mostly_best', 'random', 'human' (default), 'rules', '<model>.zip'
        player_2_type: str
            Player 2. One of 'best' (default), 'mostly_best', 'random', 'human', 'rules', '<model>.zip'
        first_player: str
            Who goes first. One of 'player_1' (default), 'player_2', 'random'
        render_mode: str or None
            How to render the game. One of 'plot' (default), 'print', None
        """

        # Connect to the probe
        IO.connect()

        # STM parameters
        self.scan_bias = scan_bias
        self.scan_setpoint = scan_setpoint
        self.passivate_setpoint = passivate_setpoint
        self.num_coarse_moves_on_reset = 2

        # Game parameters
        self.game = None
        self.game_args = {"player_1_type": player_1_type,
                          "player_2_type": player_2_type,
                          "first_player": first_player,
                          "render_mode": render_mode}
        self.old_board = None

        # Others
        self.fig = None
        self.axs = None

        self.reset()

    def play_game(self):
        pass

        # Step agent
        # If human, action = find_human_move, pass to self_play_test.step(action)

        # Draw action in STM

    def step(self):
        # Get human action
        if self.game_args["player_1_type"] == "human":
            action = self.find_human_move()

        self.draw(DataShape("cross"), centre=None)
        self.game.step(action)
        self.draw(DataShape("nought"), centre=None)

    def reset(self):
        # Reset env
        self.game = SelfPlayTester(**self.game_args)

        # Coarse move & approach
        black_box.backward()

        rand_coarse_move = np.random.rand()
        if 0 <= rand_coarse_move <= 0.25:
            move_dir = black_box.x_minus
        elif 0.25 < rand_coarse_move <= 0.5:
            move_dir = black_box.x_plus
        elif 0.5 < rand_coarse_move <= 0.75:
            move_dir = black_box.y_minus
        else:
            move_dir = black_box.y_plus
        for i in range(self.num_coarse_moves_on_reset):
            move_dir()

        black_box.auto_approach()

        # Take a single scan
        prelim_scan = self.get_scan()

        # Check if flat
        is_flat = True
        if not is_flat:
            warnings.warn("Game area is not viable! Retracting and moving!")
            self.reset()

        # Draw grid
        self.draw(DataShape("board"), centre=[512 // 2, 512 // 2])

        # Setup figs
        self.fig, self.axs = plt.subplots(1, 3)

        self.game.env._make_axs(ax=self.axs[1])
        self.game.env.fig = self.fig

        self.render()

    def get_scan(self):
        return xy_scanner.get_xy_scan("Z", "Forward", "Up")

    def find_human_move(self):
        # Locate centres of grids
        pass

    def draw(self, shape_to_draw: DataShape, centre: np.ndarray([int, int])):
        """Draws the object, centered at pos"""

        pass

    def render(self, data):
        self.game.render()
        self.axs[0].imshow(data, cmap=nanomap)
        # Draw DataShape.plot()


if __name__ == '__main__':
    # Parse args
    game = STMTicTacToe()
