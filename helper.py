from collections import Counter

from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import collection
from collections import Counter
import emoji


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    num_massages = df.shape[0]
    word = []
    for masages in df["massage"]:
        word.extend(masages.split())
    num_media_masage = df[df["massage"] == "<Media omitted>\n"].shape[0]

    extractor = URLExtract()
    links = []
    for masages in df["massage"]:
        links.extend(extractor.find_urls(masages))
    return num_massages, len(word), num_media_masage, len(links)


def fetch_busy_user(df):
    x = df["users"].value_counts().head()
    df = round((df["users"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={"count": "percent"})
    return x, df


def crete_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    f = open("stop_hinglish.txt", "r")
    stopword = f.read()
    temp = df[df["users"] != "group_notification"]
    temp = df[df["massage"] != "<Media omitted>\n"]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    df_wc = wc.generate(temp["massage"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stopword = f.read()
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    temp = df[df["users"] != "group_notification"]
    temp = df[df["massage"] != "<Media omitted>\n"]
    words = []
    for masages in temp["massage"]:
        for word in masages.lower().split():
            if word not in stopword:
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    emojis = []
    for masages in df["massage"]:
        emojis.extend([c for c in masages if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_user(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    timeline = df.groupby(["year", "month_num", "month_name"]).count()["massage"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month_name"][i] + "-" + str(timeline["year"][i]))
    timeline["time"] = time
    return timeline


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    return df["day_name"].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    return df["month_name"].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    activity_heat = df.pivot_table(index="day_name", columns="period", values="massage", aggfunc="count").fillna(0)
    return activity_heat
