from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Load the OpenAI API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/get_stock_recommendation", methods=["POST"])
def get_stock_recommendation():
    data = request.json
    user_responses = data.get("responses", [])

    # Create a prompt based on user responses
    prompt = (
        f"The user has the following investment profile:\n"
        f"1. Investment amount: {user_responses[0] if len(user_responses) > 0 else 'Not provided'}\n"
        f"2. Sector: {user_responses[1] if len(user_responses) > 1 else 'Not provided'}\n"
        f"3. Withdrawal criteria: {user_responses[2] if len(user_responses) > 2 else 'Not provided'}\n\n"
        f"Based on this profile, recommend a single stock or investment strategy."
    )

    try:
        # Use OpenAI to analyze the prompt
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        recommendation = response["choices"][0]["message"]["content"].strip()
        return jsonify({"recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
