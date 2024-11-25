@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')

        if not user_input:
            return jsonify({"response": "Invalid input. Please try again."})

        # Initial input processing
        if "current date and time" in user_input.lower():
            response = "Enter your investment preferences (e.g., 'I have $100, invest in technology, withdraw if I lose $20'):"
        else:
            # Continue to analyze preferences if date/time was already provided
            response = analyze_investment_preferences(user_input)

        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, something went wrong. Please try again."})
