import os
from flask import Flask, request, jsonify
import openai
import yfinance as yf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    print("Error: OpenAI API key not found!")

app = Flask(__name__)

# Function to analyze investment preferences
def analyze_investment_preferences(preferences):
    try:
        # Extract details from preferences (basic parsing for demo)
        industry = "technology"  # Example
        budget = 3               # Example
        risk_tolerance = 2       # Example

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

        # Build LLM prompt
        prompt = f"""
        The user has ${budget} to invest in the {industry} industry and wants to withdraw if they lose more than ${risk_tolerance}.
        Based on the following stock prices: {stock_data}, recommend one specific stock they should invest in.
        Justify your choice briefly and ensure it aligns with the user's criteria.
        """

        print(f"Prompt sent to OpenAI: {prompt}")

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in analyze_investment_preferences: {e}")
        return "Sorry, I could not analyze your preferences at this time."

# Chatbot route
@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')

        print(f"Received input: {user_input}")

        if not user_input:
            return jsonify({"response": "Invalid input. Please try again."})

        # First question
        if "current date and time" in user_input.lower() or ":" in user_input:
            response = "Enter your investment preferences (e.g., 'I have $100, invest in technology, withdraw if I lose $20'):"
        else:
            # Analyze preferences
            response = analyze_investment_preferences(user_input)

        print(f"Response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"response": "Sorry, something went wrong. Please try again."})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
