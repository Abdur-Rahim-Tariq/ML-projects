import os
import re
import tweepy
import pandas as pd
import streamlit as st
from textblob import TextBlob
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    st.error("Set your TWITTER_BEARER_TOKEN in the .env file before running the app.")
    st.stop()

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
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
def fetch_tweets(keyword, limit=30):
    try:
        limit = max(10, min(limit, 30))  # keep within safe limits for free API
        query = f"{keyword} -is:retweet lang:en"
        tweets = client.search_recent_tweets(query=query, max_results=limit)
        if not tweets.data:
            return pd.DataFrame(columns=["Tweet"])
        texts = [tweet.text for tweet in tweets.data]
        df = pd.DataFrame(texts, columns=["Tweet"])
        df["Cleaned"] = df["Tweet"].apply(clean_text)
        df["Sentiment"] = df["Cleaned"].apply(get_sentiment)
        return df
    except tweepy.TooManyRequests:
        st.error("Twitter API rate limit reached. Please wait 15 few minutes before trying again.")
        return pd.DataFrame(columns=["Tweet"])
    except Exception as e:
        st.warning(f"Error fetching tweets: {e}")
        return pd.DataFrame(columns=["Tweet"])

st.set_page_config(page_title="Twitter Sentiment Analysis", layout="centered")
st.title("Twitter Sentiment Analysis App")
st.write("Analyze the sentiment of recent tweets on any topic using TextBlob.")

keyword = st.text_input("Enter a hashtag or keyword", "#AI")
tweet_count = st.slider("Number of tweets to fetch", 10, 30, 10)

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing tweets..."):
        df = fetch_tweets(keyword, tweet_count)

    if df.empty:
        st.warning("No tweets found or rate limit reached. Try again later.")
    else:
        st.success(f"Analyzed {len(df)} tweets for '{keyword}'")
        st.subheader("Sample Tweets")
        st.dataframe(df[["Tweet", "Sentiment"]].head(10))

        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x="Sentiment", data=df, palette="viridis", ax=ax)
        plt.title("Sentiment Breakdown")
        st.pyplot(fig)

        st.subheader("Summary")
        sentiment_counts = df["Sentiment"].value_counts(normalize=True) * 100
        st.write(sentiment_counts.round(2).astype(str) + "%")

        st.subheader("Most Positive Tweet")
        st.write(df.loc[df["Cleaned"].apply(lambda x: TextBlob(x).sentiment.polarity).idxmax(), "Tweet"])

        st.subheader("Most Negative Tweet")
        st.write(df.loc[df["Cleaned"].apply(lambda x: TextBlob(x).sentiment.polarity).idxmin(), "Tweet"])
