import os
from flask import Flask, request, jsonify
import openai
import yfinance as yf

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to analyze investment preferences
def analyze_investment_preferences(preferences):
    try:
        # Example hardcoded logic for the flow (can be improved)
        industry = "technology"
        budget = 3
        risk_tolerance = 2

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

        # Build prompt for OpenAI
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
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in analyze_investment_preferences: {e}")
        return "Sorry, I couldn't analyze the preferences. Please try again."

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        if not user_input:
            return jsonify({"response": "Invalid input. Please try again."})

        # Logic to process user input and determine next steps
        if "current date and time" in user_input.lower():
            response = "Enter your investment preferences (e.g., 'I have $100, invest in technology, withdraw if I lose $20'):"
        else:
            response = analyze_investment_preferences(user_input)

        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, something went wrong. Please try again."})


if __name__ == '__main__':
    app.run(debug=True)
