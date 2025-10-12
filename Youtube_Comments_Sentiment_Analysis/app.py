import os
import re
import pandas as pd
import streamlit as st
from textblob import TextBlob
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    st.error("Please set your YOUTUBE_API_KEY in the .env file.")
    st.stop()

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    else:
        return None

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

@st.cache_data(show_spinner=False)
def fetch_comments(video_url, limit=50):
    video_id = extract_video_id(video_url)
    if not video_id:
        st.warning("Invalid YouTube URL.")
        return pd.DataFrame(columns=["Comment"])

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=limit,
            textFormat="plainText"
        )
        response = request.execute()

        comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    for item in response.get("items", [])]

        if not comments:
            return pd.DataFrame(columns=["Comment"])

        df = pd.DataFrame(comments, columns=["Comment"])
        df["Cleaned"] = df["Comment"].apply(clean_text)
        df["Sentiment"] = df["Cleaned"].apply(get_sentiment)
        return df

    except Exception as e:
        st.warning(f"Error fetching comments: {e}")
        return pd.DataFrame(columns=["Comment"])

st.set_page_config(page_title="YouTube Comment Sentiment Analysis", layout="centered")
st.title("YouTube Comment Sentiment Analysis App")
st.write("Analyze the sentiment of comments from any YouTube video using TextBlob.")

video_url = st.text_input("Enter YouTube video URL")
comment_count = st.slider("Number of comments to fetch", 10, 100, 50)

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing comments..."):
        df = fetch_comments(video_url, comment_count)

    if df.empty:
        st.warning("No comments found or API limit reached.")
    else:
        st.success(f"Analyzed {len(df)} comments")

        st.subheader("Sample Comments")
        st.dataframe(df[["Comment", "Sentiment"]].head(10))

        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x="Sentiment", data=df, palette="viridis", ax=ax)
        plt.title("Sentiment Breakdown")
        st.pyplot(fig)

        st.subheader("Summary")
        sentiment_counts = df["Sentiment"].value_counts(normalize=True) * 100
        st.write(sentiment_counts.round(2).astype(str) + "%")

        st.subheader("Most Positive Comment")
        st.write(df.loc[df["Cleaned"].apply(lambda x: TextBlob(x).sentiment.polarity).idxmax(), "Comment"])

        st.subheader("Most Negative Comment")
        st.write(df.loc[df["Cleaned"].apply(lambda x: TextBlob(x).sentiment.polarity).idxmin(), "Comment"])
