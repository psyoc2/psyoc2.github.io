from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_recommendation', methods=['POST'])
def get_stock_recommendation():
    try:
        # Retrieve user inputs from the form
        user_input = request.json.get('user_input')
        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        # Send the user's input to OpenAI for processing
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a stock investment advisor."},
                {"role": "user", "content": user_input}
            ]
        )

        # Parse and return the response from OpenAI
        recommendation = response['choices'][0]['message']['content']
        return jsonify({"recommendation": recommendation})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
