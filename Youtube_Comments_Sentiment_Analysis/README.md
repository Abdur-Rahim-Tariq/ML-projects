🎥 YouTube Comment Sentiment Analysis App

Analyze sentiments of YouTube comments in real-time using Streamlit, TextBlob, and the YouTube Data API.
This app allows users to input any YouTube video URL and instantly visualize whether comments are Positive, Negative, or Neutral.

🚀 Features

🔍 Fetches comments directly using the YouTube Data API

🧹 Cleans and preprocesses text automatically

🧠 Performs sentiment analysis using TextBlob

📊 Visualizes sentiment breakdown using Seaborn

💬 Displays the most positive and most negative comments

🎨 Simple, interactive, and beginner-friendly Streamlit UI

🧠 How It Works

Enter a YouTube video URL.

Fetch comments through the YouTube API.

Clean and preprocess the comments.

Use TextBlob to determine sentiment polarity (range: -1 → 1).

Classify each comment as:

✅ Positive

⚪ Neutral

❌ Negative

Display results with tables and visual charts.

🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web app framework
TextBlob	Sentiment analysis
Google API Client	Fetching YouTube comments
Matplotlib / Seaborn	Data visualization
dotenv	Environment variable management
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/Abdur-Rahim-Tariq/youtube-sentiment-analysis.git
cd youtube-sentiment-analysis

2️⃣ Create and activate a virtual environment
python -m venv env
# For Windows
env\Scripts\activate
# For macOS/Linux
source env/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your YouTube API key

Create a file named .env in the project root:

YOUTUBE_API_KEY=your_youtube_api_key_here

5️⃣ Run the app
streamlit run app.py

📊 Example Output

Sentiment Distribution Example:

Positive — 60%
Neutral — 25%
Negative — 15%


The app shows:

🧩 Data table of analyzed comments

📈 Sentiment distribution bar chart

🏆 Most positive and negative comments

🧰 Folder Structure
📦 youtube-sentiment-analysis
 ┣ 📜 app.py
 ┣ 📜 requirements.txt
 ┣ 📜 .env
 ┗ 📜 README.md

💡 Future Enhancements

🤖 Upgrade to transformer-based models (e.g., BERT) for accuracy

☁️ Deploy on Streamlit Cloud

🌍 Support for multi-language comments

☁️ Add live YouTube comment streaming

📬 Contact

👤 Abdur Rahim Tariq

📧 Email: abdurrahimtariq.ds@gmail.com

🐙 GitHub: Abdur-Rahim-Tariq

💼 LinkedIn: linkedin.com/in/abdurrahim-tariq