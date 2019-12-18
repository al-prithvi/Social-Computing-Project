import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


def get_data_from_csv():
    return pd.read_csv("../data/USvideos.csv")


def delete_duplicates(df):
    df = df.drop_duplicates(subset='video_id', keep='first')
    return df


def get_videos_titles():
    data = pd.read_csv("../data/USvideos.csv")
    cleaned_data = delete_duplicates(data)
    titles = cleaned_data['title']
    return titles


def get_video_title_lengths(titles):
    titles = titles.map(lambda x: re.sub(r"[^\w']|_", ' ', x))  # remove special characters but keep apostrophes
    counts = titles.str.split().str.len()
    return counts


def get_stats(df):
    values = df['length'].sort_values()
    values_mean = values.mean().round().astype(int)
    values_median = values.median().astype(int)
    values_mode = values.mode()[0]
    values_range = [values.min(), values.max()]
    return values_mean, values_median, values_mode, values_range


def make_graph(df):
    unique, counts = np.unique(df['length'], return_counts=True)
    fig = plt.figure()
    plt.barh(unique, counts, align='center', alpha=0.75)
    plt.yticks(unique)
    plt.xlabel('Count')
    plt.ylabel('Title Length')
    plt.title('Video Title Lengths')
    plt.show()

    fig.savefig('video_title_lengths.png')


if __name__ == "__main__":
    df = pd.DataFrame()
    df['title'] = get_videos_titles()
    df['length'] = get_video_title_lengths(df['title'])

    # print(df)

    make_graph(df)

    mean, median, mode, the_range = get_stats(df)

    print("Mean: ", mean)
    print("Median: ", median)
    print("Mode: ", mode)
    print("Range: ", the_range)
    print("Total Values: ", df.shape[0])

