import pandas as pd
import numpy as np
from datetime import datetime
import pytz
from math import ceil
import matplotlib.pyplot as plt
from matplotlib import cm

import seaborn as sns

sns.set_style("white")



def get_data_from_csv():
    return pd.read_csv("../data/USvideos.csv")


def delete_duplicates(df):
    df = df.sort_values('views', ascending=True)
    df = df.drop_duplicates(subset='video_id', keep='first')
    return df


def find_all_collabs(df):
    li = []
    for index, row in df.iterrows():
        title = row["title"].lower().strip()
        if (" ft" in title or " feat" in title or " feature" in title or " featuring" in title) \
                and ("featurette" not in title):
            temp = {}
            # temp["title"] = title
            temp["video_id"] = row["video_id"]
            # temp["channel"] = row["channel_title"]
            li.append(temp)
    return pd.DataFrame(li)



def collab_finder():
    df = get_data_from_csv()
    df = delete_duplicates(df)
    new_df = find_all_collabs(df)

    final_df = pd.merge(df, new_df, how="inner", on="video_id")
    final_df.to_csv('../data/collab_list.csv', index=None, header=True)




if __name__ == "__main__":
    collab_finder()