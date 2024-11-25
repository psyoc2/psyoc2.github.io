from flask import Flask, request, jsonify
import openai
import yfinance as yf
import os

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/process", methods=["POST"])
def process():
    try:
        # Get user message from the frontend
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Example: Handle the investment-related input
        if "Enter the current date and time" in user_input:
            return jsonify({"response": "What are your investment preferences?"})

        # Example: Parse and process investment preferences
        elif "I have" in user_input and "invest" in user_input:
            preferences = user_input
            # Example: Extract values from user input (dummy values here)
            budget = 3
            risk_tolerance = 2
            industry = "technology"

            # Fetch stock data
            tech_stocks = ["AAPL", "MSFT", "GOOGL", "AMD", "NVDA"]
            stock_data = {}
            for stock in tech_stocks:
                try:
                    ticker = yf.Ticker(stock)
                    history = ticker.history(period="1y")
                    if not history.empty:
                        stock_data[stock] = history["Close"].iloc[-1]  # Last closing price
                except Exception as e:
                    print(f"Error fetching data for {stock}: {e}")

            # Build OpenAI prompt
            prompt = f"""
            The user has ${budget} to invest in the {industry} industry and wants to withdraw if they lose more than ${risk_tolerance}.
            Based on the following stock prices: {stock_data}, recommend one specific stock they should invest in.
            Justify your choice briefly and ensure it aligns with the user's criteria.
            """

            # Generate recommendation
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return jsonify({"response": response['choices'][0]['message']['content']})

        else:
            return jsonify({"response": "Sorry, I didn't understand your input. Could you clarify?"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Sorry, something went wrong. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)
