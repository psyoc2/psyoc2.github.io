from flask import Flask, request, jsonify, render_template
import openai
import os
import yfinance as yf
from datetime import datetime

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found in environment variables.")

app = Flask(__name__)

# Session state for managing conversation flow
session_state = {
    "step": 0,
    "current_time": None,
    "investment_preferences": None,
}

# Function to analyze investment preferences and recommend a stock
def analyze_investment_preferences(preferences):
    # Extracted preferences for this example
    industry = "technology"  # Can be parsed from preferences
    budget = 3               # Can be parsed from preferences
    risk_tolerance = 2       # Can be parsed from preferences

    # Fetch market data for top technology stocks
    tech_stocks = ["AAPL", "MSFT", "GOOGL", "AMD", "NVDA"]  # Example stocks
    stock_data = {}

    for stock in tech_stocks:
        try:
            ticker = yf.Ticker(stock)
            history = ticker.history(period="1y")
            if not history.empty:
                stock_data[stock] = history["Close"].iloc[-1]  # Use last closing price
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")

    # Build LLM prompt with investment details and stock data
    prompt = f"""
    The user has ${budget} to invest in the {industry} industry and wants to withdraw if they lose more than ${risk_tolerance}. 
    Based on the following stock prices: {stock_data}, recommend one specific stock they should invest in. 
    Justify your choice briefly and ensure it aligns with the user's criteria.
    """

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    # Return recommendation
    return response['choices'][0]['message']['content']


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global session_state
    user_input = request.json.get("message")
    step = session_state["step"]

    if step == 0:
        session_state["current_time"] = user_input
        session_state["step"] += 1
        return jsonify({"response": "Enter your investment preferences (e.g., 'I have $57, invest in sports for 5 months and withdraw if I lose $27')."})

    elif step == 1:
        session_state["investment_preferences"] = user_input
        session_state["step"] += 1

        # Analyze investment preferences and generate stock recommendation
        recommendation = analyze_investment_preferences(session_state["investment_preferences"])
        return jsonify({"response": f"Based on your input, here is the stock recommendation:\n{recommendation}"})

    return jsonify({"response": "I did not understand. Please refresh and start again."})


if __name__ == "__main__":
    app.run(debug=True)
