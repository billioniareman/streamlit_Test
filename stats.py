# import matplotlib.pyplot as plt
from collections import Counter

import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud


# fetch statistics
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df["message"]:
        words.extend(message.split())
    num_media = df[df['message'] == "<Media omitted>\n"].shape[0]
    links = []
    extraction = URLExtract()
    for message in df['message']:
        links.extend(extraction.find_urls(message))
    return num_messages, len(words), num_media, len(links)


# fetch most busy user
def most_busy_user(df):
    users = df['user'].value_counts().head()
    df = round(((df['user'].value_counts() / df['user'].shape[0]) * 100), 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percentage'})
    return users, df


# Wordcloud
def word_cloud(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    updated_df = df[df['user'] != "Group Notification"]
    updated_df = updated_df[updated_df["message"] != "<Media omitted>\n"]

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)

    wc = WordCloud(width=300, height=300, background_color='white', min_font_size=10)
    updated_df["message"] = updated_df["message"].apply(remove_stop_words)
    df_wc = wc.generate(updated_df['message'].str.cat(sep=" "))
    return df_wc


# most common words
def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    updated_df = df[df['user'] != "Group Notification"]
    updated_df = updated_df[updated_df["message"] != "<Media omitted>\n"]

    words = []
    for message in updated_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_analyzer(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    emoji_list = []
    for message in df['message']:
        emoji_list.extend([c for c in message if emoji.emoji_count(c)])
    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))
    return emoji_df


def month_analyzer(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
