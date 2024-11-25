from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)

# Load .env file
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
