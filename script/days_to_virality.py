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


def extract_date(str_date):
    date_list = str_date.split(".")
    year = "20" + date_list[0]
    day = date_list[1]
    month = date_list[2]
    return datetime.strptime(year + "-" + month + "-" + day, '%Y-%m-%d')


def fix_date_formats(df):
    df["publish_time"] = pd.to_datetime(df["publish_time"], infer_datetime_format=True)
    ls = []
    for index, row in df.iterrows():
        ls.append(extract_date(row["trending_date"]))
    df["trending_date_parsed"] = ls
    return df


def extract_top_10_videos_per_month(df):
    video_dict = {}
    for i in range(1, 13):
        video_dict[str(i)] = []
    for index, row in df.iterrows():
        # TODO need to work from here
        video_dict[str(row["publish_month"])].append(row.to_dict())
    for i in range(1, 13):
        if len(video_dict[str(i)]) == 0:
            del video_dict[str(i)]
    sorted_dict = {}
    for key, value in video_dict.items():
        sorted_dict[key] = sorted(video_dict[key], key=lambda i: i['views'], reverse=True)[:10]
    final_df = pd.DataFrame()
    frames = []
    columns = ['video_id', 'trending_date', 'title', 'channel_title', 'category_id', 'publish_time', 'tags', 'views',
               'likes', 'dislikes', 'comment_count', 'thumbnail_link', 'comments_disabled', 'ratings_disabled',
               'video_error_or_removed', 'description', 'publish_month']

    for key, value in sorted_dict.items():
        temp_df = pd.DataFrame(value)
        frames.append(temp_df)
    final_df = pd.concat(frames)
    final_df.to_csv('../data/top_10_per_month.csv', index=None, header=True)


def count_days_to_virality(df):
    final_dict = {}
    df['publish_time'].apply(lambda x: datetime.replace(x, tzinfo=None))
    for index, row in df.iterrows():
        time_to_virality = (row["trending_date_parsed"].value - row["publish_time"].value) / ((10 ** 9) * 86400)
        if time_to_virality < 1:
            final_dict["< 1"] = final_dict.get("< 1", 0) + 1
        elif time_to_virality < 2:
            final_dict["1 - 2"] = final_dict.get("1 - 2", 0) + 1
        elif time_to_virality < 3:
            final_dict["2 - 3"] = final_dict.get("2 - 3", 0) + 1
        elif time_to_virality < 4:
            final_dict["3 - 4"] = final_dict.get("3 - 4", 0) + 1
        elif time_to_virality < 5:
            final_dict["3 - 4"] = final_dict.get("3 - 4", 0) + 1
        elif time_to_virality < 7:
            final_dict["5 - 7"] = final_dict.get("5 - 7", 0) + 1
        elif time_to_virality < 10:
            final_dict["7 - 10"] = final_dict.get("7 - 10", 0) + 1
        elif time_to_virality < 20:
            final_dict["10 - 20"] = final_dict.get("10 - 20", 0) + 1
        else:
            final_dict[">= 20"] = final_dict.get(">= 20", 0) + 1
    sorted_final_dict = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_final_dict


def build_bar_graph(video_days_to_virality):
    fig = plt.figure()
    x = []
    y = []
    for i in range(0, len(video_days_to_virality)):
        x.append(video_days_to_virality[i][0])
        y.append(video_days_to_virality[i][1])
    plt.bar(x, y, align='center', alpha=0.75)
    plt.xticks(x)
    plt.ylabel('Count')
    plt.xlabel('Time Taken(Days)')
    plt.title('Number of Days for the Video to go Viral vs Count')
    plt.show()
    fig.savefig('days_to_virality.png')


def get_days_to_virality():
    data_csv = get_data_from_csv()
    cleaned_data = delete_duplicates(data_csv)
    cleaned_data = fix_date_formats(cleaned_data)
    video_days_to_virality = count_days_to_virality(cleaned_data)
    build_bar_graph(video_days_to_virality)


def get_categories_of_country():
    category_df = pd.read_json("../data/US_category_id.json")
    category_dict = {}
    for i in category_df["items"]:
        x = str(i["id"])
        title = i["snippet"]["title"]
        category_dict[x] = title
    category_df_csv = pd.DataFrame(list(category_dict.items()))
    category_df_csv.to_csv("../data/categories_usa.csv", index=None, header=True)


def retrieve_categories():
    return pd.read_csv("../data/categories_usa.csv").to_dict()


if __name__ == "__main__":
    get_days_to_virality()
