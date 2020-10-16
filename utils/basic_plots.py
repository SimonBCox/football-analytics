# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


# ## ------------------------- ## #
# ## Functions to Create plots ## #
# ## ------------------------- ## #

def create_pitch(length: int = 120, width: int = 80, fig=None, ax=None):
    """
    This script is copied from https://fcpython.com/visualisation/drawing-pitchmap-adding-lines-circles-matplotlib
    This function plots a football pitch with the possibility to input the dimensions.
    :return: plot of a football pitch with provided or default dimensions
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
    pitch_length = 120
    pitch_width = 80

    # ## Create test events
    # Start with empty DataFrames
    pass_events = pd.DataFrame()
    carry_events = pd.DataFrame()

    # Generate random start and end locations
    start_locations = pd.DataFrame(np.random.randint(0, 100, size=(50, 2)), columns=["1", "2"])
    end_locations = pd.DataFrame(np.random.randint(0, 100, size=(50, 2)), columns=["1", "2"])
    start_locations["1"] = start_locations["1"] * pitch_length
    start_locations["2"] = start_locations["2"] * pitch_width
    end_locations["1"] = start_locations["1"] * pitch_length
    end_locations["2"] = start_locations["2"] * pitch_width

    # Merge start and end locations into lists [x_start, y_start] [x_end, y_end]
    pass_events["location"] = start_locations.values.tolist()
    pass_events["pass_end_location"] = end_locations.values.tolist()
    pass_events["type_name"] = "Pass"
    pass_events["player_name"] = "Dr. Gino"

    carry_events = pass_events.rename(columns={"pass_end_location": "carry_end_location"})
    carry_events["type_name"] = "Carry"

    # Test pass map
    create_pass_map(events=pass_events)
    plt.show()

    # Test carry map
    create_carry_map(events=carry_events)
    plt.show()
