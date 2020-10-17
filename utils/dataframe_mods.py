# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import math
import pandas as pd
import numpy as np


# ## ------------------------------- ## #
# ## Functions to modify data frames ## #
# ## ------------------------------- ## #

def map_location(x: pd.DataFrame):
    """
    This function returns the location of an event as a list. If the event has no location [NaN, NaN] is returned
    :param x: a data frame containing events
    :return location: a list containing the location coordinates of an event
    """
    if x.location == x.location:
        location = x.location
    else:
        location = [np.nan, np.nan]
    return location


def map_end_location(x: pd.DataFrame):
    """
    This function returns the end location of an event as a list containing its x, y, and z coordinates. If an end
    location has no z coordinate [x, y, NaN] is returned. If the event has nog end location [NaN, NaN, NaN] is returned.
    :param x: a data frame containing events
    :return end_location: a list containing the end location coordinates of an event
    """
    try:
        end_location = x[f'{x.type_name.lower()}_end_location']
        # Make sure list of three values is returned [x_end, y_end, z_end]
        if len(end_location) == 2:
            end_location.append(np.nan)
    except KeyError:
        end_location = [np.nan, np.nan, np.nan]
    return end_location


def map_dx_dy(x: pd.DataFrame):
    """
    This function returns the distance between a start and end location of an event in the form of a list containing
    delta x and delta y.
    distance.
    :param x: a data frame containing events
    :return dx_dy: a list containing the distance between the start and end location of an event
    """
    try:
        dx_dy = [x.x_end - x.x_start, x.y_end - x.y_start]
    except KeyError:
        dx_dy = [np.nan, np.nan]
    return dx_dy


def map_outcome(x: pd.DataFrame):
    """
    This function returs the outcome of an event. If an event has no outcome Nan is returned
    :param x: a data frame containing events
    :return outcome: a string describing the outcome of an event or NaN
    """
    try:
        outcome = x[f'{x.type_name.lower()}_outcome_name']
    except KeyError:
        outcome = np.nan
    return outcome


def add_carry_info(data: pd.DataFrame):
    """
    This function groups the event data by player and adds the following carry information to the data frame.
    Number of carries, matches played, total distance carried, maximum distance carried in one carry, average distance
    carried per match.
    :param data: a data frame containing events
    :return data_grouped: a data frame containing information on carries grouped by player
    """
    # Calculate distance per carry
    data["distance_carried"] = data.apply(lambda x: round(math.sqrt((x.location[0] - x.carry_end_location[0]) ** 2 +
                                                                    (x.location[1] - x.carry_end_location[1]) ** 2))
    if type(x.carry_end_location) == list else 0, axis=1)

    # Count events per type grouped by players
    data_grouped = data.groupby(['type_name'])["player_name"].value_counts().unstack().transpose()
    data_grouped = data_grouped.rename(columns={"Carry": "Nr. of Carries"})

    # Calculate number of matches played and total distance carried
    data_grouped[["Matches Played", "Total Distance Carried"]] = data.groupby('player_name').agg(
        {"match_id": "nunique", "distance_carried": "sum"})

    # Calculate maximum distance carried in one match
    data_grouped["Max. Distance in One Match"] = data.groupby(["player_name", "match_id"]).agg(
        {'distance_carried': "sum"}).unstack().max(axis=1)

    # Calculate average distance carried per match
    data_grouped["Avg. Distance per Match"] = data_grouped["Nr. of Carries"].divide(
        data_grouped["Matches Played"]).round(1)

    return data_grouped


def get_dribble_info(data: pd.DataFrame, sort_by: str = "Complete", ascending: bool = False):
    """
    This function creates a data frame containing information on dribbles per player. The created data frame contains
    the following information: total number of dribbles, number of complete dribbles, number of incomplete dribbles,
    the dribble success rate, number of matches played, average number of dribbles per match, the success rate ranking,
    and the average dribbles per match ranking.
    :param data: a data frame containing events
    :param sort_by: a string describing on which column of the new created data frame should be sorted
    :param ascending: a boolean setting the sorting direction, ascending or descending
    :return dribble_data: a data frame containing information on dribbles grouped by player
    """
    # Get number of complete and imcomplete dribbles
    dribble_data = data[data.type_name == "Dribble"].groupby("player_name")[
        "dribble_outcome_name"].value_counts().unstack()

    # Add total dribbles
    dribble_data.insert(0, "Total dribbles", dribble_data["Complete"] + dribble_data["Incomplete"])

    # Add succes rate
    dribble_data["Success rate"] = round(
        dribble_data["Complete"] / (dribble_data["Incomplete"] + dribble_data["Complete"]), 2)

    # Add matches played
    dribble_data["Matches played"] = data.groupby("player_name")['match_id'].nunique()

    # Add dribbles per match
    dribble_data["Dribbles per match"] = round(
        (dribble_data["Incomplete"] + dribble_data["Complete"]) / dribble_data["Matches played"], 1)

    if dribble_data.shape[0] > 1:
        # Add ranking
        dribble_data[["Success rate ranking", "Dribbles per match ranking"]] = dribble_data[
            ["Success rate", "Dribbles per match"]].rank(ascending=False)

    # Rename index
    dribble_data = dribble_data.sort_values(sort_by, ascending=ascending).reset_index().rename_axis("Index", axis=1)

    return dribble_data


def dribble_map_index(data: pd.DataFrame, player: str = None, event: str = None):
    """
    This function creates a mask, i.e. a list of booleans, to filter an specified event and the two events prior and two
    events successive to the specified event.
    :param data: a data frame containing event data
    :param player: a string containing the name of the player of interest
    :param event: a string containing the event of interest
    :return mapping: a list of booleans which can be used as a mask to filter the events data frame
    """
    mapping = ((((data['type_name'] == event) & (data['player_name'] == player)) |
                ((data.shift(+1)['type_name'] == event) &
                 (data['player_name'].shift(+1) == player) & (abs(data['index'] - data['index'].shift(+1)) < 5)) |
                ((data.shift(+2)['type_name'] == event) &
                 (data['player_name'].shift(+2) == player) & (abs(data['index'] - data['index'].shift(+2)) < 5)) |
                ((data.shift(-1)['type_name'] == event) &
                 (data['player_name'].shift(-1) == player) & (abs(data['index'] - data['index'].shift(-1)) < 5)) |
                ((data.shift(-2)['type_name'] == event) &
                 (data['player_name'].shift(-2) == player) & (abs(data['index'] - data['index'].shift(-2)) < 5))))
    return mapping
