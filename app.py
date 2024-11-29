from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)

# Load .env fileimport streamlit as st
import openai
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from sentiment_analysis import SentimentAnalyzer

# Initialize the SentimentAnalyzer with the dataset
sentiment_analyzer = SentimentAnalyzer("path/to/twitter-financial-news-sentiment.csv")

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Custom styles for Streamlit
st.markdown(
    """
    <style>
    body {
        background-color: #5A189A;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    .stApp {
        background-color: #5A189A;
    }
    h1, h2, h3 {
        color: #E0E0E0;
        font-family: 'Courier New', Courier, monospace;
    }
    p {
        color: #FFFFFF;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #FFC300;
        color: #000000;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        font-family: Arial, sans-serif;
    }
    .stButton>button:hover {
        background-color: #FFB000;
    }
    .stTextInput>div>input {
        background-color: #9932CC;
        color: white;
        font-family: Arial, sans-serif;
    }
    .stMarkdown p {
        font-family: Arial, sans-serif;
        font-size: 16px;
    }
    .stSuccess {
        color: #00FF00;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.title("StockFriend: Your Investment Companion")

# Introduction
st.markdown(
    """
    ### Hello, I hope you are having a lovely day. My name is StockFriend, and I am here at your service!

    Please tell me the details of what investment you want to make, and I will use my algorithms to assist you!

    An example of what you could say is: **"I have $53.60 I want to invest, please choose 3 stocks for me to invest in, investing $10 in 2 of them and the rest of the money in the last. I want to sell the stock once I have made $60."**

    You can provide as much detail as you like, and I'll analyze it and get my algorithms working for you!

    **Current date and time:** {}
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

# User input
user_input = st.text_area("Enter your investment preferences here:", height=100)

# Custom date input
st.markdown("### Customize Stock Data Retrieval Date Range (Optional):")
start_date = st.date_input("Start Date", value=None)
end_date = st.date_input("End Date", value=None)

# Agent selection
st.markdown("### Select the agent(s) you want to use:")
use_lstm = st.checkbox("Long Short-Term Memory (LSTM)")
use_heuristic = st.checkbox("Heuristic Algorithms")
use_technical = st.checkbox("Technical Analysis (includes multiple agents)")
use_sentiment = st.checkbox("Sentiment Analysis of financial-related tweets and news")
use_real_stockbroker = st.checkbox("Real Stockbroker")
use_llm = st.checkbox("Large Language Model (LLM)")

# Button to submit user input
if st.button("Submit"):
    if user_input.strip():
        try:
            # Define stock data retrieval date range
            if start_date and end_date:
                custom_start_date = start_date.strftime("%Y-%m-%d")
                custom_end_date = end_date.strftime("%Y-%m-%d")
                st.markdown(f"### Using custom date range: {custom_start_date} to {custom_end_date}")
            else:
                custom_start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
                custom_end_date = datetime.now().strftime("%Y-%m-%d")
                st.markdown(f"### Using default date range: {custom_start_date} to {custom_end_date}")

            # Analyze user input
            tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN"]
            stock_data = {}

            for stock in tech_stocks:
                ticker = yf.Ticker(stock)
                history = ticker.history(start=custom_start_date, end=custom_end_date)
                if not history.empty:
                    stock_data[stock] = history["Close"]

            agent_used = None  # Track which agent was used

            # Decision-making based on selected agents
            if use_sentiment:
                agent_used = "Sentiment Analysis of financial-related tweets and news"
                st.markdown(f"### Using {agent_used} for Recommendation")
                sentiments = {}
                for stock in tech_stocks:
                    sentiments[stock] = sentiment_analyzer.get_sentiment_for_stock(stock)

                high_sentiment_threshold = 1.5  # Example threshold for positive sentiment
                low_sentiment_threshold = 0.5  # Example threshold for negative sentiment
                sentiment_based_recommendations = [
                    stock for stock, sentiment in sentiments.items()
                    if sentiment is not None and (sentiment >= high_sentiment_threshold or sentiment <= low_sentiment_threshold)
                ]

                if sentiment_based_recommendations:
                    st.write("Based on strong sentiment scores, here are the recommended stocks:")
                    for stock in sentiment_based_recommendations:
                        st.success(f"Stock: {stock}, Sentiment Score: {sentiments[stock]:.2f}")
                        # Plot stock performance
                        if stock_data.get(stock) is not None:
                            plt.figure(figsize=(10, 5))
                            plt.plot(stock_data[stock].index, stock_data[stock].values, label=f"{stock} Closing Price")
                            plt.title(f"{stock} Performance Over Custom Date Range")
                            plt.xlabel("Date")
                            plt.ylabel("Price (USD)")
                            plt.legend()
                            st.pyplot(plt)
                else:
                    st.warning("No strong sentiment data available. Consider selecting another agent.")

            elif use_llm:
                agent_used = "Large Language Model (LLM)"
                st.markdown(f"### Using {agent_used} for Recommendation")
                # OpenAI prompt
                prompt = f"""
                The user provided the following input: "{user_input}".
                Based on this input and the following stock data for the period {custom_start_date} to {custom_end_date}: {stock_data},
                recommend one stock or multiple stocks to invest in. Justify the recommendation.
                """
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                )
                recommendation = response['choices'][0]['message']['content'].replace("$", "\\$")

                # Display the GPT-based recommendation
                st.markdown("### Here is the best stock recommendation based on your input:")
                st.success(recommendation)

                # Extract stock tickers mentioned in the response
                mentioned_stocks = [stock for stock in tech_stocks if stock in recommendation]
                if mentioned_stocks:
                    for stock in mentioned_stocks:
                        plt.figure(figsize=(10, 5))
                        plt.plot(stock_data[stock].index, stock_data[stock].values, label=f"{stock} Closing Price")
                        plt.title(f"{stock} Performance Over Custom Date Range")
                        plt.xlabel("Date")
                        plt.ylabel("Price (USD)")
                        plt.legend()
                        st.pyplot(plt)
                else:
                    st.warning("No stocks explicitly mentioned in the recommendation for plotting.")

            else:
                # Default agent: LLM
                agent_used = "Large Language Model (LLM) (default)"
                st.markdown(f"### No specific agent selected, defaulting to {agent_used}.")
                # OpenAI prompt
                prompt = f"""
                The user provided the following input: "{user_input}".
                Based on this input and the following stock data for the period {custom_start_date} to {custom_end_date}: {stock_data},
                recommend one stock or multiple stocks to invest in. Justify the recommendation.
                """
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                )
                recommendation = response['choices'][0]['message']['content'].replace("$", "\\$")

                # Display the GPT-based recommendation
                st.markdown("### Here is the best stock recommendation based on your input:")
                st.success(recommendation)

                # Extract stock tickers mentioned in the response
                mentioned_stocks = [stock for stock in tech_stocks if stock in recommendation]
                if mentioned_stocks:
                    for stock in mentioned_stocks:
                        plt.figure(figsize=(10, 5))
                        plt.plot(stock_data[stock].index, stock_data[stock].values, label=f"{stock} Closing Price")
                        plt.title(f"{stock} Performance Over Custom Date Range")
                        plt.xlabel("Date")
                        plt.ylabel("Price (USD)")
                        plt.legend()
                        st.pyplot(plt)
                else:
                    st.warning("No stocks explicitly mentioned in the recommendation for plotting.")

            # Inform the user about the agent used
            st.markdown(f"### The following agent was used for decision-making: **{agent_used}**")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter your investment preferences.")

if st.button("Start New Analysis"):
    st.experimental_rerun()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/process', methods=['POST'])
def process():
    try:
        # Get the user's message from the POST request
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Call OpenAI API with the user's message
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message}
            ],
        )
        bot_response = response['choices'][0]['message']['content']
        return jsonify({"response": bot_response})

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
