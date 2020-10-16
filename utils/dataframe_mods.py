# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import math
import pandas as pd
import numpy as np


# ## ------------------------------- ## #
# ## Functions to modify data frames ## #
# ## ------------------------------- ## #

def map_location(x):
    if x.location == x.location:
        location = x.location
    else:
        location = [np.nan, np.nan]
    return location


def map_end_location(x):
    try:
        end_location = x[f'{x.type_name.lower()}_end_location']
        # Make sure list of three values is returned [x_end, y_end, z_end]
        if len(end_location) == 2:
            end_location.append(np.nan)
    except KeyError:
        end_location = [np.nan, np.nan, np.nan]
    return end_location


def map_dx_dy(x):
    try:
        dx_dy = [x.x_end - x.x_start, x.y_end - x.y_start]
    except KeyError:
        dx_dy = [np.nan, np.nan]
    return dx_dy


def map_outcome(x):
    try:
        outcome = x[f'{x.type_name.lower()}_outcome_name']
    except KeyError:
        outcome = np.nan
    return outcome


def add_carry_info(data: pd.DataFrame):
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


def get_dribble_info(data: pd.DataFrame, sort_by: str="Complete", ascending: bool=False):
    '''
    '''
    # Get number of complete and imcomplete dribbles
    dribble_data = data[data.type_name=="Dribble"].groupby("player_name")["dribble_outcome_name"].value_counts().unstack()
    
    # Add total dribbles
    dribble_data.insert(0, "Total dribbles", dribble_data["Complete"] + dribble_data["Incomplete"])
    
    # Add succes rate
    dribble_data["Success rate"] = round(dribble_data["Complete"]/(dribble_data["Incomplete"] + dribble_data["Complete"]),2)
    
    # Add matches played
    dribble_data["Matches played"] = data.groupby("player_name")['match_id'].nunique()
    
    # Add dribbles per match
    dribble_data["Dribbles per match"] = round((dribble_data["Incomplete"] + dribble_data["Complete"])/dribble_data["Matches played"],1)
    
    if dribble_data.shape[0] > 1:
        # Add ranking
        dribble_data[["Success rate ranking", "Dribbles per match ranking"]] = dribble_data[["Success rate", "Dribbles per match"]].rank(ascending=False)
            
    # Rename index
    dribble_data = dribble_data.sort_values(sort_by, ascending=ascending).reset_index().rename_axis("Index", axis=1)
    
    return dribble_data


def dribble_map_index(df: pd.DataFrame, player: str=None, event: str=None):
    mapping = ((((df['type_name'] == event) & (df['player_name'] == player)) |
                ((df.shift(+1)['type_name'] == event) & 
                 (df['player_name'].shift(+1) == player) & (abs(df['index'] - df['index'].shift(+1)) < 5)) |
                ((df.shift(+2)['type_name'] == event) &
                 (df['player_name'].shift(+2) == player) & (abs(df['index'] - df['index'].shift(+2)) < 5)) |
                ((df.shift(-1)['type_name'] == event) &
                 (df['player_name'].shift(-1) == player) & (abs(df['index'] - df['index'].shift(-1)) < 5)) |
                ((df.shift(-2)['type_name'] == event) &
                 (df['player_name'].shift(-2) == player) & (abs(df['index'] - df['index'].shift(-2)) < 5))))
    return mapping