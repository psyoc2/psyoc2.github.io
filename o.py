import yfinance as yf
import openai
import os
from datetime import datetime

# Set your OpenAI API Key

# Function to analyze investment preferences and recommend a stock
def analyze_investment_preferences(preferences):
    # Parse user input (basic parsing for demo purposes, can be improved)
    industry = "technology"  # Extracted from preferences
    budget = 3               # Extracted from preferences
    risk_tolerance = 2       # Extracted from preferences
    
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

# Main function
def main():
    try:
        # Get user inputs
        current_time = input("Enter the current date and time (YYYY-MM-DD HH:MM:SS): ")
        preferences = input(
            "Enter investment preferences (e.g., 'I have $57, invest in sports for 5 months and withdraw if I lose $27'): "
        )

        # Analyze and recommend a stock
        recommendation = analyze_investment_preferences(preferences)

        # Display recommendation
        print("Recommended investment:")
        print(recommendation)

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script
if __name__ == "__main__":
    main()
