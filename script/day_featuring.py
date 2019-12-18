import pandas as pd
from datetime import datetime
import pytz
import json
import numpy as np
import matplotlib.pyplot as plt
import re


def get_data_from_csv():
    return pd.read_csv("../data/USvideos.csv")

def get_data_from_json():
    return pd.read_json("../data/US_category_id.json")


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

def collab():
    print("Hello Social Computing Project")
    data_csv2 = get_data_from_csv()
    data_csv = delete_duplicates(data_csv2)
    #print(data_csv)
    #print(data_csv.columns)
    columns = ['video_id', 'trending_date', 'title', 'channel_title', 'category_id', 'publish_time', 'tags', 'views',
               'likes', 'dislikes', 'comment_count', 'thumbnail_link', 'comments_disabled', 'ratings_disabled',
               'video_error_or_removed', 'description', 'publish_month']


    # Titles
    titles = (data_csv.iloc[:,2])
    descript = (data_csv.iloc[:,columns.index('description')])
    cnt = 0
    tot = 0
    # file for writing descriptions of videos without featuring
    f= open("description_of_vids.txt","w+")

    cnt_of_follows = 0
    cnt_of_fb = 0
    cnt_of_tw = 0
    cnt_of_tblr = 0
    cnt_of_snap = 0
    cnt_of_insta = 0
    list_of_counts = [0, 0, 0, 0, 0, 0]

    for ev in titles:
        ev = ev.lower()
        tot+=1

        follow_total = 0

        if ('feat.' in ev.lower()) or ('ft.' in ev.lower()) or ('featuring' in ev.lower()):
            #print(ev)
            cnt+=1
            #print(ev)

        '''
        else:
                f.write(str(ev))
                f.write("\n----------------------\n\n")   
        '''    
            #print(ev, " : ", descript.iloc[tot-1])
        # '''
        follows = re.findall(r"Follow.*?on", str(descript.iloc[tot-1])  )
        if len(follows) > 0:
            cnt_of_follows+=1
        if 'facebook' in str(descript.iloc[tot-1]).lower():
            cnt_of_fb += 1
            follow_total += 1

            if (len(follows) == 0):
                f.write(str(ev)+"-> "+str(descript.iloc[tot-1]))
                f.write("\n----------------------\n\n")



        if 'twitter' in str(descript.iloc[tot-1]).lower():
            cnt_of_tw += 1           
            follow_total += 1
        if 'tumblr' in str(descript.iloc[tot-1]).lower():
            cnt_of_tblr += 1
            follow_total += 1
        if 'snapchat' in str(descript.iloc[tot-1]).lower():
            cnt_of_snap += 1
            follow_total += 1
        if 'instagram' in str(descript.iloc[tot-1]).lower():
            cnt_of_insta += 1
            follow_total += 1
        # '''

        list_of_counts[follow_total] += 1

    print("Follow total: ", list_of_counts)
    print(sum(list_of_counts))            

    print("Count of ft/feat etc = ", cnt, " out of ", tot)
    # checks for the "follow us on tag, but i guess it's useless"
    print("Count of follows = ", cnt_of_follows)
    print("Count of FB = ", cnt_of_fb)
    print("Count of Twitter = ", cnt_of_tw)
    print("Count of Tumblr = ", cnt_of_tblr)
    print("Count of snapchat = ", cnt_of_snap)
    print("Count of instagram = ", cnt_of_insta)

    # plot 1
    #list for plotting
    platform_counts = []
    platform_counts.append(cnt_of_fb)
    platform_counts.append(cnt_of_tw)
    platform_counts.append(cnt_of_tblr)
    platform_counts.append(cnt_of_snap)
    platform_counts.append(cnt_of_insta)
    li = ["Tumblr", "Snapchat", "Instagram", "Facebook", "Twitter"]
    (platform_counts.sort())
    plt.bar(range(len(platform_counts)), [val for val in platform_counts], align='center')
    plt.xticks(range(len(li)), [val for val in li])#rotation = 45)
    #plt.xticks(rotation=70)

    #labels
    plt.title("Platforms linked in description")
    plt.ylabel('Video Count')
    plt.xlabel('Social media platforms linked')
    plt.tight_layout()
    #plt.show()
    plt.savefig('CountVSWhich Platforms.png')



    plt.clf()


    '''cleaned_data = delete_duplicates(data_csv)
    cleaned_data = fix_date_formats(cleaned_data)
    extract_top_10_videos_per_month(cleaned_data)'''
 
    # plot 2
    li = ["0", "1", "2", "3", "4", "5"]
    plt.bar(range(len(list_of_counts)), [val for val in list_of_counts], align='center')
    plt.xticks(range(len(li)), [val for val in li])#rotation = 45)
    #plt.xticks(rotation=70)

    #labels
    plt.title("Count of social media platforms linked")
    plt.ylabel('Video Count')
    plt.xlabel('Number of social media platforms linked')
    plt.tight_layout()
    #plt.show()
    plt.savefig('CountVSPlatforms.png')

def date_find():
    data_csv2 = get_data_from_csv()
    data_csv = delete_duplicates(data_csv2)
    # print(data_csv)
    print(data_csv.columns)

    # Titles
    dt_list = ((data_csv.loc[:,'publish_time']))
    cnt = 0
    dic = {}
    for dt in dt_list:
        cnt+=1
        dtobj = datetime.strptime(dt[:10], '%Y-%m-%d')
        key = dtobj.weekday()

        if key in dic:
            dic[key] += 1
        else:
            dic[key] = 1
    print("count: ", cnt, " and len(list)= ", len(dic))
    print("\n\n\n")
    print(dict(sorted(dic.items())))
    print("\n\n\n")
    print("checking sum of all the frequencies")
    sm = 0
    list_freq = list(range(7))

    for k,v in dic.items():
        sm += v
        print(k, " : ", v)

        list_freq[k] = v # for plotting
    print("Count of Videos: ", sm)

    # plot 
    li = ["M", "T", "W", "Th", "F", "Sa", "Su"]
    plt.bar(range(len(list_freq)), [val for val in list_freq], align='center')
    plt.xticks(range(len(li)), [val for val in li])
    #plt.xticks(rotation=70)

    #labels
    plt.title("Count of viral videos per day of the week")
    plt.ylabel('Count of Videos')
    plt.xlabel('Day of the week')
    plt.tight_layout()
    #plt.show()
    plt.savefig('CountVSDay.png')


def get_categories_of_country():
    category_df = pd.read_json("../data/US_category_id.json")
    category_dict = {}
    for i in category_df["items"]:
        x = str(i["id"])
        title = i["snippet"]["title"]
        category_dict[x] = title
    category_df_csv = pd.DataFrame(list(category_dict.items()))
    category_df_csv.to_csv("../data/categories_usa.csv", index=None, header=True)


if __name__ == "__main__":
    # colloboration video count
    collab()
    print("\n\n\n")
    # day of the week vs video count
    #date_find()
    
    # get_categories_of_country()