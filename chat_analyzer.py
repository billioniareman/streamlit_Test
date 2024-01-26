import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import preprocessor
import stats

st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a chat file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove("Group Notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis",user_list)
    if st.sidebar.button("Show Analysis"):
        #statistics
        num_messages ,words,num_media,links = stats.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("Links shared")  
            st.title(links)
    #Timeline
        #monthly timeline
        st.title("Monthly analysis")
        timeline=stats.month_analyzer(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline
        st.title('Daily analysis')
        daily_timeline=stats.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #activity map
        st.title('User Activity')
        col1,col2=st.columns(2)
        with col1:
            st.title('Active day')
            active_day=stats.week_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(active_day.index,active_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Active month')
            active_month=stats.month_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(active_month.index,active_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #Activity heatmap
        st.title("Weekly activity map")
        user_heatmap=stats.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #busiest user in chat(Group level)
        if selected_user=='Overall':
            st.title('Most active user')
            users,new_df=stats.most_busy_user(df)
            fig,ax= plt.subplots()
            col1,col2 =st.columns(2)
            with col1:
                ax.bar(users.index,users.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #Wordcloud
        st.title('Word Cloud')
        df_wc = stats.word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        #most common words
        st.title("Most used words")
        return_df=stats.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(return_df[0],return_df[1])
        st.pyplot(fig)
        #emoji analyzer
        st.title('Most used emoji')
        emoji_df=stats.emoji_analyzer(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)