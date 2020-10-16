# ## ------- ## #
# ## Imports ## #
# ## ------- ## #

import sys
import time
import json
import pandas as pd


# ## ----------------------- ## #
# ## Functions to load JSONs ## #
# ## ----------------------- ## #

def load_json(path: str):
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)
    df = pd.json_normalize(data, sep="_")

    return df


def load_multiple_json(path: str, df: pd.DataFrame, join_on: str):
    df_list = []
    total = len(df[join_on])
    start_time = time.time()

    for i, item in enumerate(df[join_on]):
        df = load_json(f"{path}{item}.json")
        df_list.append(df.assign(new_col=item))

        # plot progress bar
        time_passed = round(time.time() - start_time, 1)
        etr = round(time_passed / ((i + 1) / total) - time_passed, 1)
        progress_bar(i, total - 1, status=f'Loading {total} jsons. '
                                          f'Time passed: {time_passed} sec. '
                                          f'Time remaining: {etr} sec')
        time.sleep(0.5)

    concat_df = pd.concat(df_list)
    concat_df = concat_df.rename(columns={"new_col": join_on})
    return concat_df


# Progress bar by Vladimir Ignatyev. Source: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress_bar(count, total, status=''):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()