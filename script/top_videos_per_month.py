import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import cm

def get_data_from_csv():
    return pd.read_csv("../data/USvideos.csv")


def delete_duplicates(df):
    df = df.sort_values('views', ascending=False)
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
    for index, row in df.iterrows():
        row["trending_date"] = extract_date(row["trending_date"])
    indexes = df[df['publish_time'] < datetime(2017, 12, 1, tzinfo=pytz.UTC)].index
    df.drop(indexes, inplace=True)
    df['publish_month'] = df['publish_time'].dt.month
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


def get_top_videos_per_month():
    print("Hello Social Computing Project")
    data_csv = get_data_from_csv()
    cleaned_data = delete_duplicates(data_csv)
    cleaned_data = fix_date_formats(cleaned_data)
    extract_top_10_videos_per_month(cleaned_data)


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


def build_category_counts():
    data_csv = get_data_from_csv()
    cleaned_data = delete_duplicates(data_csv)
    categories = retrieve_categories()
    categories = categories["category_title"]
    category_title_list = []
    for index, row in cleaned_data.iterrows():
        try:
            category_title_list.append(categories[int(row["category_id"])])
        except:
            category_title_list.append("Others")
    cleaned_data["category_title"] = category_title_list
    value, counts = np.unique(cleaned_data['category_title'], return_counts=True)
    count_sort_ind = np.argsort(-counts)
    value = value[count_sort_ind]
    counts = counts[count_sort_ind]

    # plt.bar(value, counts, align='center', alpha=0.5)
    # plt.xticks(value)
    # plt.ylabel('Count')
    # plt.title('Categories')

    #
    # colors = cm.hsv(counts / float(max(counts)))
    # plot = plt.scatter(counts, counts, c=counts, cmap='hsv')
    # plt.clf()
    # plt.colorbar(plot)

    fig = plt.figure()
    # plt.barh(value, counts, align='center', alpha=0.75, color = colors)
    plt.barh(value, counts, align='center', alpha=0.75)
    plt.yticks(value)
    plt.xlabel('Viral Video Count')
    plt.ylabel('Genre of Videos')
    plt.title('Viral Videos by Genre')

    plt.show()


    fig.savefig('category_counts_2.png')


if __name__ == "__main__":
    # get_top_videos_per_month()
    # get_categories_of_country()
    build_category_counts()
