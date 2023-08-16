import streamlit as st
import processor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer Sachin")

Upload_file = st.sidebar.file_uploader("Chose a file")
if Upload_file is not None:
    bytes_data = Upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = processor.preprocessor(data)

    # fetch unique user
    user_list = df["users"].unique().tolist()

    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_massages, word, num_media_masage, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Massages")
            st.title(num_massages)
        with col2:
            st.header("Total Words")
            st.title(word)
        with col3:
            st.header("Media Shared")
            st.title(num_media_masage)
        with col4:
            st.header("Links Shared")
            st.title(links)

        timeline = helper.monthly_user(selected_user, df)

        # Create a Streamlit figure
        st.title("Monthly Massages Trend")
        fig, ax = plt.subplots()

        ax.plot(timeline["time"], timeline["massage"], color="green")
        ax.set_xticklabels(timeline["time"], rotation="vertical")  # Set x-axis tick labels

        ax.set_title('Monthly Messages')
        plt.tight_layout()

        # Display the plot using Streamlit
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            ax.set_xticklabels(busy_day.index, rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            ax.set_xticklabels(busy_month.index, rotation="vertical")
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        st.title("Most Busy users")

        if selected_user == "Overall":
            x, new_df = helper.fetch_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col1:
                st.dataframe(new_df)
        st.title("Word Cloud")
        df_wc = helper.crete_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        st.title("Top 20 Most Used Words")
        return_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(return_df[0], return_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
