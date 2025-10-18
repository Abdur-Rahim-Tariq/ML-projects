# 🐦 Twitter Sentiment Analysis App

Analyze the sentiments of recent tweets in real time using **Streamlit**, **Tweepy**, and **TextBlob**.  
This app allows users to input any **keyword or hashtag**, fetch recent tweets, and visualize whether they are **Positive**, **Negative**, or **Neutral**.

---

## 🚀 Features

- 🔍 Fetches live tweets via the **Twitter API v2**
- 🧹 Cleans and preprocesses text automatically
- 🧠 Performs sentiment analysis using **TextBlob**
- 📊 Visualizes sentiment breakdown using **Seaborn**
- 💬 Displays the **most positive** and **most negative** tweets

---

## 🧠 How It Works

1. Enter a **keyword** or **hashtag** (e.g., `#AI`, `Python`, `OpenAI`).  
2. The app fetches recent English tweets using the **Twitter API v2**.  
3. Each tweet is cleaned and analyzed with **TextBlob** for sentiment polarity.  
4. Tweets are classified as:
   - ✅ **Positive**
   - ⚪ **Neutral**
   - ❌ **Negative**
---

## 🛠️ Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Python** | Core programming language |
| **Streamlit** | Web application framework |
| **Tweepy** | Fetches live tweets using the Twitter API |
| **TextBlob** | Sentiment analysis |
| **Matplotlib / Seaborn** | Data visualization |
| **dotenv** | Environment variable management |
