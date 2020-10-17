# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import matplotlib.pyplot as plt
from matplotlib.patches import Arc


# ## ------------------------- ## #
# ## Functions to Create plots ## #
# ## ------------------------- ## #

def create_pitch(length: int = 120, width: int = 80, fig=None, ax=None):
    """
    This script is copied from https://fcpython.com/visualisation/drawing-pitchmap-adding-lines-circles-matplotlib
    This function plots a football pitch with the possibility to input the dimensions.
    :param length: an integer describing the length of the pitch
    :param width: an integer describing the width of the pitch
    :param fig: a figure as template for the
    :param ax: a subplot of the figure on which to plot the pitch
    :return fig, ax: plot of a football pitch
    """

    # Create figure if needed
    if not fig:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, width], color="black")
    plt.plot([0, length], [width, width], color="black")
    plt.plot([length, length], [width, 0], color="black")
    plt.plot([length, 0], [0, 0], color="black")
    plt.plot([length / 2, length / 2], [0, width], color="black")

    # Left Penalty Area
    plt.plot([16.5, 16.5], [width / 2 + 20, width / 2 - 20], color="black")
    plt.plot([0, 16.5], [width / 2 + 20, width / 2 + 20], color="black")
    plt.plot([16.5, 0], [width / 2 - 20, width / 2 - 20], color="black")

    # Right Penalty Area
    plt.plot([length, length - 16.5], [width / 2 + 20, width / 2 + 20], color="black")
    plt.plot([length - 16.5, length - 16.5], [width / 2 + 20, width / 2 - 20], color="black")
    plt.plot([length - 16.5, length], [width / 2 - 20, width / 2 - 20], color="black")

    # Left 6-yard Box
    plt.plot([0, 5.5], [width / 2 + 9, width / 2 + 9], color="black")
    plt.plot([5.5, 5.5], [width / 2 + 9, width / 2 - 9], color="black")
    plt.plot([5.5, 0], [width / 2 - 9, width / 2 - 9], color="black")

    # Right 6-yard Box
    plt.plot([length, length - 5.5], [width / 2 + 9, width / 2 + 9], color="black")
    plt.plot([length - 5.5, length - 5.5], [width / 2 + 9, width / 2 - 9], color="black")
    plt.plot([length - 5.5, length], [width / 2 - 9, width / 2 - 9], color="black")

    # Prepare Circles
    centre_circle = plt.Circle((length / 2, width / 2), 9.15, color="black", fill=False)
    centre_spot = plt.Circle((length / 2, width / 2), 0.8, color="black")
    left_pen_spot = plt.Circle((11, width / 2), 0.8, color="black")
    right_pen_spot = plt.Circle((length - 11, width / 2), 0.8, color="black")

    # Draw Circles
    ax.add_patch(centre_circle)
    ax.add_patch(centre_spot)
    ax.add_patch(left_pen_spot)
    ax.add_patch(right_pen_spot)

    # Prepare Arcs
    left_arc = Arc((11, width / 2),
                   height=18.3, width=18.3, angle=0, theta1=307, theta2=53, color="black")
    right_arc = Arc((length - 11, width / 2),
                    height=18.3, width=18.3, angle=0, theta1=127, theta2=232, color="black")

    # Draw Arcs
    ax.add_patch(left_arc)
    ax.add_patch(right_arc)

    # Tidy Axes
    plt.axis('off')

    return fig, ax


if __name__ == "__main__":
    # Figure
    fig = plt.figure()

    # Subplot 1 with standard dimensions
    ax1 = plt.subplot(1, 2, 1)
    create_pitch(fig=fig, ax=ax1)

    # Subplot 2 with custom dimensions
    ax2 = plt.subplot(1, 2, 2)
    create_pitch(length=90, width=50, fig=fig, ax=ax2)

