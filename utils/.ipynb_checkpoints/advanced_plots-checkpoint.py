# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from math import pi
from utils.basic_plots import create_pitch


# ## -------------- ## #
# ## Advanced Plots ## #
# ## -------------- ## #
from utils.dataframe_mods import map_location, map_end_location, map_dx_dy, map_outcome


def create_arrow_map(events: pd.DataFrame, event_type: str = "Pass", match: str = "an unknown match", fig=None, ax=None,
                     pitch_length: int = 120, pitch_width: int = 80, color: str = "blue"):
    """
    This functions creates a map of arrows between the start point and end point of an event.
    :return: map of a pitch with event arrows
    """

    # Filter only relevant events
    temp_df = events[events.type_name == event_type]

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


def create_heat_map(events: pd.DataFrame, match: str = "an unknown match", fig=None, ax=None,
                    pitch_length: int = 120, pitch_width: int = 80):
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


def create_extended_regplot(data: pd.DataFrame, x: str = None, y: str = None, top_n: int = 2,
                            player_to_highlight: str = None, fig=None, ax=None):
    if x is None or y is None:
        print("Please provide what to plot: x-axis and y-axis")
        return

    if not fig:
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(1, 1, 1)

    sns.regplot(x=x, y=y, data=data, ci=100, color='steelblue')

    if top_n:
        top_n_match = data.loc[data.groupby(x)[y].nlargest(top_n).unstack().columns]
        ax.scatter(top_n_match[x], top_n_match[y], color='green')
        labels = top_n_match
    else:
        labels = data

    if player_to_highlight:
        ax.scatter(top_n_match.loc[player_to_highlight][x], top_n_match.loc[player_to_highlight][y],
                   color='darkorange', marker="*", s=300, alpha=0.8)

    for name, values in labels.iterrows():
        ax.annotate(name, (values[x], values[y]), ha='center', va="bottom")

    ax.set_ylim(0)
    ax.set_ylabel('')
    ax.set_title(y)

    return fig, ax


def create_event_map(data: pd.DataFrame, fig=None, ax=None, pitch_length: int = 120, pitch_width: int = 80):
    # Draw pitch
    fig, ax = create_pitch(pitch_length, pitch_width, fig, ax)

    # For all events get type, start and end location, and determine outcome
    locations = pd.DataFrame(data.apply(lambda x: map_location(x), axis=1).to_list(), columns=['x_start', 'y_start'])
    locations['type_name'] = pd.DataFrame(data['type_name'].to_list())
    locations[['x_end', 'y_end', 'z_end']] = pd.DataFrame(data.apply(lambda x: map_end_location(x), axis=1).to_list())
    locations[['dx', 'dy']] = pd.DataFrame(locations.apply(lambda x: map_dx_dy(x), axis=1).to_list())
    locations['outcome'] = pd.DataFrame(data.apply(lambda x: map_outcome(x), axis=1).to_list())

    # Plot
    for event_type in locations.type_name.unique():
        temp = locations[locations['type_name'] == event_type]

        if event_type == 'Ball Receipt*':
            temp.plot(kind='scatter', x='x_start', y='y_start', marker='o', s=50, color='tab:cyan',
                      label='Ball Receipt', alpha=1, ax=ax, zorder=2)

        if event_type == 'Carry':
            temp.plot(kind='scatter', x='x_start', y='y_start', marker='p', s=40, color='blue',
                      label='Carry', alpha=1, ax=ax, zorder=0)
            for i, event in temp.iterrows():
                ax.arrow(event.x_start, event.y_start, event.dx, event.dy, head_width=0.5, ls=':', color='blue',
                         alpha=1, zorder=0, length_includes_head=True)

        if event_type == 'Dribble':
            complete = temp[temp['outcome'] == 'Complete']
            incomplete = temp[temp['outcome'] == 'Incomplete']

            complete.plot(kind='scatter', x='x_start', y='y_start', marker='X', s=75, color='tab:green',
                          label='Complete Dribble', alpha=1, ax=ax, zorder=3, lw=0.5, edgecolor='black')
            incomplete.plot(kind='scatter', x='x_start', y='y_start', marker='X', s=75, color='tab:red',
                            label='Incomplete Dribble', alpha=1, ax=ax, zorder=3, lw=0.5, edgecolor='black')

        if event_type == 'Pass':
            complete = temp[temp['outcome'] != 'Incomplete']
            incomplete = temp[temp['outcome'] == 'Incomplete']

            complete.plot(kind='scatter', x='x_start', y='y_start', marker='h', s=50, color='lightsalmon',
                          alpha=1, ax=ax, zorder=1, label='Complete Pass')
            incomplete.plot(kind='scatter', x='x_start', y='y_start', marker='h', s=50, color='slategrey', alpha=1,
                            ax=ax, zorder=1, label='Incomplete Pass')

            for i, event in complete.iterrows():
                ax.arrow(event.x_start, event.y_start, event.dx, event.dy, head_width=0.5, ls='-', color='lightsalmon',
                         alpha=1, zorder=0, length_includes_head=True)
            for i, event in incomplete.iterrows():
                ax.arrow(event.x_start, event.y_start, event.dx, event.dy, head_width=0.5, ls='-', color='slategrey',
                         alpha=1, zorder=0, length_includes_head=True)

        if event_type == 'Shot':
            goals = temp[temp['outcome'] == 'Goal']
            misses = temp[temp['outcome'] != 'Goal']
            goals.plot(kind='scatter', x='x_start', y='y_start', marker='*', s=75, color='orange',
                       label='Goal!', alpha=1, ax=ax, zorder=3, lw=0.5, edgecolor='black')
            misses.plot(kind='scatter', x='x_start', y='y_start', marker='*', s=75, color='slategrey',
                        label='Missed Shot', alpha=1, ax=ax, zorder=3, lw=0.5, edgecolor='black')

    return fig, ax


def create_radar_chart(data: pd.DataFrame, ax=None, color: str = 'blue'):
    # Based on script by FC PYTHON, source: "https://fcpython.com/visualisation/radar-charts-matplotlib"

    # Get attributes, data, and angles
    attributes = sorted(data.type_name.unique())

    angles = list(np.arange(0, 2*pi, 2*pi/len(attributes)))
    angles += angles[:1]
    dat = data.type_name.value_counts().loc[attributes].to_list()
    dat += dat[:1]

    # Create plot
    if not ax:
        ax = plt.subplot(111, polar=True)

    # Plot polyline and fill
    ax.plot(angles, dat)
    ax.fill(angles, dat, color=color, alpha=0.1)

    # Add labels and player name
    plt.xticks(angles[:-1], attributes)
    plt.figtext(0.2, 0.9, data.player_name.unique()[0], color=color)

    ax.set_rscale('log')

    return ax
