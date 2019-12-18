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


def count_days_of_virality_day_wise(df):
    value, count = np.unique(df['video_id'], return_counts=True)
    count.sort()
    return put_in_bins_day_wise(count)

def count_days_of_virality_week_wise(df):
    value, count = np.unique(df['video_id'], return_counts=True)
    count.sort()
    return put_in_bins_week_wise(count)

def put_in_bins_week_wise(count):
    count_dict = {}
    for i in count:
        video_count = int(i)
        if video_count <= 7:
            count_dict["<= 1"] = count_dict.get("1", 0) + 1
        elif video_count <= 14:
            count_dict["1 - 2"] = count_dict.get("1 - 2", 0) + 1
        elif video_count <= 21:
            count_dict["2 - 3"] = count_dict.get("2 - 3", 0) + 1
        else:
            count_dict[">3"] = count_dict.get(">3", 0) + 1
    return count_dict


def put_in_bins_day_wise(count):
    count_dict = {}
    for i in count:
        video_count = int(i)
        if video_count == 1:
            count_dict["1"] = count_dict.get("1", 0) + 1
        elif video_count == 2:
            count_dict["2"] = count_dict.get("2", 0) + 1
        elif video_count == 3:
            count_dict["3"] = count_dict.get("3", 0) + 1
        elif video_count == 4:
            count_dict["4"] = count_dict.get("4", 0) + 1
        elif video_count == 5:
            count_dict["5"] = count_dict.get("5", 0) + 1
        elif video_count == 6:
            count_dict["6"] = count_dict.get("6", 0) + 1
        elif video_count == 7:
            count_dict["7"] = count_dict.get("7", 0) + 1
        elif video_count > 8 and video_count <= 10:
            count_dict["8 - 10"] = count_dict.get("8 - 10", 0) + 1
        elif video_count > 11 and video_count <= 15:
            count_dict["11 - 15"] = count_dict.get("11 - 15", 0) + 1
        elif video_count > 16 and video_count <= 20:
            count_dict["16 - 20"] = count_dict.get("16 - 20", 0) + 1
        elif video_count <= 25:
            count_dict["21 - 25"] = count_dict.get("21 - 25", 0) + 1
        else:
            count_dict[">25"] = count_dict.get(">25", 0) + 1
    return count_dict


def build_bar_graph(days_of_virality, filename, metric):
    fig = plt.figure()
    d = days_of_virality
    x = []
    y = []
    print("days", days_of_virality)
    '''for k,v in days_of_virality.items():
        x.append(k)
        y.append(v)
    '''
    rot = None
    if len(d) == 4:
        x = ["<= 1", "1 - 2", "2 - 3", ">3"]
        rot = 0
    else:
        x = ["1", "2", "3", "4", "5", "6", "7", "8 - 10", "11 - 15", "16 - 20" \
        , "21 - 25", ">25"]
        rot = 45
    for k in x:
        y.append(d[k])

    plt.bar(range(len(y)), y)

    plt.xticks(range(len(x)), x, rotation=rot)
    #plt.xticks(x, rotation=45)
    #plt.bar(x, y, align='center', alpha=0.75)
    #plt.xticks(x, rotation=45)
    plt.ylabel('Count of Videos')
    plt.xlabel('Number of {0} a Video was Viral'.format(metric))
    plt.title('Number of {0} a Video was Viral vs Video Count'.format(metric))
    plt.tight_layout()
    plt.show()
    fig.savefig(filename)



def get_days_of_virality():
    data_csv = get_data_from_csv()
    days_of_virality = count_days_of_virality_day_wise(data_csv)
    build_bar_graph(days_of_virality, 'days_of_virality_day_wise.png', "Days")

    weeks_of_virality = count_days_of_virality_week_wise(data_csv)
    build_bar_graph(weeks_of_virality, 'days_of_virality_week_wise.png', "Weeks")


if __name__ == "__main__":
    get_days_of_virality()
