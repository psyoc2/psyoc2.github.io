import os
import openai
import yfinance as yf
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Retrieve OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this variable is set securely in your hosting environment

# Flask route to render the chatbot interface
@app.route("/")
def index():
    return render_template("index.html")

# Initialize a session state
session_state = {
    "step": 0,
    "current_time": None,
    "preferences": None,
    "final_recommendation": None,
}

# Route to handle user input and respond
@app.route("/chat", methods=["POST"])
def chat():
    global session_state

    user_input = request.json.get("message", "")
    response = ""

    # Step 0: Ask for the current date and time
    if session_state["step"] == 0:
        response = "Please enter the current date and time (YYYY-MM-DD HH:MM:SS):"
        session_state["step"] = 1

    # Step 1: Save the entered date/time and ask for investment preferences
    elif session_state["step"] == 1:
        try:
            datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")  # Validate date format
            session_state["current_time"] = user_input
            response = (
                "Enter your investment preferences (e.g., 'I have $50, invest in technology and withdraw if I lose $10'):"
            )
            session_state["step"] = 2
        except ValueError:
            response = "Invalid date format. Please use YYYY-MM-DD HH:MM:SS."

    # Step 2: Analyze investment preferences and recommend a stock
    elif session_state["step"] == 2:
        session_state["preferences"] = user_input

        # Analyze preferences and call OpenAI API if needed
        recommendation = analyze_investment_preferences(session_state["preferences"])
        session_state["final_recommendation"] = recommendation

        response = f"Recommended investment: {recommendation}"

        # Reset for next conversation
        session_state["step"] = 0

    return jsonify({"response": response})

# Function to analyze investment preferences and recommend a stock
def analyze_investment_preferences(preferences):
    # Basic parsing (could be enhanced with NLP tools)
    industry = "technology"  # Hardcoded as an example
    budget = 3  # Replace with extracted budget
    risk_tolerance = 2  # Replace with extracted tolerance

    # Fetch stock data
    tech_stocks = ["AAPL", "MSFT", "GOOGL", "AMD", "NVDA"]
    stock_data = {}

    for stock in tech_stocks:
        try:
            ticker = yf.Ticker(stock)
            history = ticker.history(period="1y")
            if not history.empty:
                stock_data[stock] = history["Close"].iloc[-1]
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")

    # Prepare OpenAI prompt
    prompt = f"""
    The user has ${budget} to invest in the {industry} industry and wants to withdraw if they lose more than ${risk_tolerance}.
    Based on the following stock prices: {stock_data}, recommend one specific stock they should invest in.
    Justify your choice briefly and ensure it aligns with the user's criteria.
    """

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
