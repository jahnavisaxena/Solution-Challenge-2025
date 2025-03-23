from flask import Flask, render_template, request, jsonify
import requests
import os  # For environment variables (optional)

app = Flask(__name__)

# Store your API key securely (recommended: set it in an environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        age = data.get('age')
        job = data.get('job')

        if not age or not job:
            return jsonify({"error": "Age and job fields are required"}), 400

        # Construct the AI prompt
        prompt = f"Generate a personalized career plan for a {age}-year-old working as a {job}."

        # Gemini API request payload
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        headers = {"Content-Type": "application/json"}

        # Send request to Gemini API
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch response from Gemini API"}), 500

        result = response.json()

        # Extract AI-generated text
        generated_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response from AI.")

        return jsonify({"generated_text": generated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
