# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Arc


# ## --------- ## #
# ## Functions ## #
# ## --------- ## #

def create_pitch(pitch_length: int=130, pitch_width: int=90, fig=None, ax=None):
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
    plt.plot([0, 0], [0, pitch_width], color="black")
    plt.plot([0, pitch_length], [pitch_width, pitch_width], color="black")
    plt.plot([pitch_length, pitch_length], [pitch_width, 0], color="black")
    plt.plot([pitch_length, 0], [0, 0], color="black")
    plt.plot([pitch_length/2, pitch_length/2], [0, pitch_width], color="black")

    # Left Penalty Area
    plt.plot([16.5, 16.5], [pitch_width/2+20, pitch_width/2-20], color="black")
    plt.plot([0, 16.5], [pitch_width/2+20, pitch_width/2+20], color="black")
    plt.plot([16.5, 0], [pitch_width/2-20, pitch_width/2-20], color="black")

    # Right Penalty Area
    plt.plot([pitch_length, pitch_length-16.5], [pitch_width/2+20, pitch_width/2+20], color="black")
    plt.plot([pitch_length-16.5, pitch_length-16.5], [pitch_width/2+20, pitch_width/2-20], color="black")
    plt.plot([pitch_length-16.5, pitch_length], [pitch_width/2-20, pitch_width/2-20], color="black")

    # Left 6-yard Box
    plt.plot([0, 5.5], [pitch_width/2 + 9, pitch_width/2 + 9], color="black")
    plt.plot([5.5, 5.5], [pitch_width/2 + 9, pitch_width/2 - 9], color="black")
    plt.plot([5.5, 0], [pitch_width/2 - 9, pitch_width/2 - 9], color="black")

    # Right 6-yard Box
    plt.plot([pitch_length, pitch_length-5.5], [pitch_width/2 + 9, pitch_width/2 + 9], color="black")
    plt.plot([pitch_length-5.5, pitch_length-5.5], [pitch_width/2 + 9, pitch_width/2 - 9], color="black")
    plt.plot([pitch_length-5.5, pitch_length], [pitch_width/2 - 9, pitch_width/2 - 9], color="black")

    # Prepare Circles
    centre_circle = plt.Circle((pitch_length/2, pitch_width/2), 9.15, color="black", fill=False)
    centre_spot = plt.Circle((pitch_length/2, pitch_width/2), 0.8, color="black")
    left_pen_spot = plt.Circle((11, pitch_width/2), 0.8, color="black")
    right_pen_spot = plt.Circle((pitch_length-11, pitch_width/2), 0.8, color="black")

    # Draw Circles
    ax.add_patch(centre_circle)
    ax.add_patch(centre_spot)
    ax.add_patch(left_pen_spot)
    ax.add_patch(right_pen_spot)

    # Prepare Arcs
    left_arc = Arc((11, pitch_width/2),
                   height=18.3, width=18.3, angle=0, theta1=307, theta2=53, color="black")
    right_arc = Arc((pitch_length-11, pitch_width/2),
                    height=18.3, width=18.3, angle=0, theta1=127, theta2=232, color="black")

    # Draw Arcs
    ax.add_patch(left_arc)
    ax.add_patch(right_arc)

    # Tidy Axes
    plt.axis('off')
    return fig, ax


def create_arrow_map(events: pd.DataFrame, event_type: str="Pass", match: str="a unknown match", fig=None, ax=None,
                     pitch_length: int=130, pitch_width: int=90, color: str="blue"):
    """
    This functions creates a map of arrows indicating between the start point and end point of an event.
    :return: map of a pitch with event arrows
    """

    if not isinstance(events, pd.DataFrame):
        warnings.warn(f"Wrong input for events. Expected pd.DataFrame, got {type(events)}")
        return

    # Filter only relevant events
    temp_df = events[events.type_name==event_type]
    
    # Filter start and end locations
    locations = pd.DataFrame(temp_df.location.to_list(), columns=['x_start', 'y_start'])
    locations[['x_end', 'y_end']] = pd.DataFrame(temp_df[f'{event_type.lower()}_end_location'].to_list())    

    # Add delta_x and delta_y
    locations['dx'] = locations.x_end - locations.x_start
    locations['dy'] = locations.y_end - locations.y_start
    
    # Draw pitch
    fig, ax = create_pitch(pitch_length, pitch_width, fig, ax)
    
    # Draw arrows
    for i, event in locations.iterrows():
        x_start, y_start, x_end, y_end, dx, dy = list(event)
        pass_circle = plt.Circle((x_start, y_start), 2, color=color)
        pass_circle.set_alpha(0.2)
        pass_arrow = plt.Arrow(x_start, y_start, dx, dy, width=3, color=color)
        ax.add_patch(pass_circle)
        ax.add_patch(pass_arrow)
                
    # Set limits
    plt.ylim(0, pitch_width)
    plt.xlim(0, pitch_length)
    
    plt.title(f"{event_type} map of {events.player_name.unique()[0]} during {match}")

    return fig, ax


def create_heat_map(events: pd.DataFrame, match: str = "a unknown match", fig=None, ax=None, pitch_length: int = 130, pitch_width: int = 90):
    # Draw pitch
    fig, ax = create_pitch(pitch_length, pitch_width, fig, ax)
                           
    # Filter locations and draw heatmap
    location = pd.DataFrame(events.loc[~pd.isnull(events.location)].location.to_list(), columns=['start', 'end'])
    sns.kdeplot(location.start, location.end, shade=True, n_levels=10, color="green")
                           
    # Set limits
    plt.ylim(0, pitch_width)
    plt.xlim(0, pitch_length)

    plt.title(f"Heatmap of {events.player_name.unique()[0]} during {match}")

    return fig, ax


if __name__ == "__main__":
    pitch_length = 130
    pitch_width = 90

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
