import unittest
from unittest.mock import patch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from MH import MH

class TestMH(unittest.TestCase):
    def setUp(self):
        self.mh = MH()

    def test_plot(self):
        # Create a mock plot object
        mock_plot = patch.object(plt, 'plot').start()

        # Call the plot function
        self.mh.plot()

        # Assert that the plot function was called with the correct arguments
        mock_plot.assert_called_with([1], [0.0], label="switch", color="red")
        mock_plot.assert_called_with([1], [0.0], label="stay", color="blue")

        # Stop the patch
        patch.stopall()

    def test_animate_plot(self):
        # Create a mock animation object
        mock_animation = patch.object(animation, 'FuncAnimation').start()

        # Call the animate_plot function
        self.mh.animate_plot()

        # Assert that the FuncAnimation constructor was called with the correct arguments
        mock_animation.assert_called_with(plt.figure(), self.mh.animate, frames=self.mh.n_trials, interval=10, repeat=False)

        # Stop the patch
        patch.stopall()

if __name__ == "__main__":
    unittest.main()