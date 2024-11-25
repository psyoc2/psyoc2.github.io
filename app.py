import os
import openai
from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

# Use the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to track the conversation state
conversation_state = {
    "current_step": 0,  # Tracks which question to ask next
    "responses": {}     # Stores responses to previous questions
}

# Questions flow
questions = [
    "Enter the current date and time (YYYY-MM-DD HH:MM:SS):",
    "How much money do you have to invest?",
    "What is your risk tolerance (e.g., 'I want to withdraw if I lose $5')?",
    "What industry would you like to invest in (e.g., technology, healthcare)?"
]

def analyze_investment_preferences(responses):
    budget = responses.get("budget", 0)
    risk_tolerance = responses.get("risk_tolerance", 0)
    industry = responses.get("industry", "technology")

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

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error analyzing investment preferences: {str(e)}"

@app.route("/process", methods=["POST"])
def process():
    global conversation_state

    # Get user input from frontend
    data = request.json
    user_response = data.get("message", "")

    # Determine the current step
    current_step = conversation_state["current_step"]

    if current_step == 0:  # Asking for the date and time
        conversation_state["responses"]["date_time"] = user_response
    elif current_step == 1:  # Asking for the budget
        conversation_state["responses"]["budget"] = user_response
    elif current_step == 2:  # Asking for risk tolerance
        conversation_state["responses"]["risk_tolerance"] = user_response
    elif current_step == 3:  # Asking for industry
        conversation_state["responses"]["industry"] = user_response

    # Move to the next step
    conversation_state["current_step"] += 1

    # If all steps are complete, process investment preferences
    if conversation_state["current_step"] >= len(questions):
        recommendation = analyze_investment_preferences(conversation_state["responses"])
        return jsonify({"message": recommendation})

    # Otherwise, send the next question
    next_question = questions[conversation_state["current_step"]]
    return jsonify({"message": next_question})

if __name__ == "__main__":
    app.run(debug=True)
