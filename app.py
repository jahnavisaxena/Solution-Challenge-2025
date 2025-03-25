from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the Gemini API key
GEMINI_API_KEY = os.environ.get("AIzaSyAQaz1GUX8i3A3XPq-wAhB1e4260eGH7JY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Initialize the Gemini API with your API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        age = data.get('age')
        profession = data.get('profession')

        if not age or not profession:
            return jsonify({"error": "Age and profession fields are required"}), 400

        # Construct the AI prompt
        prompt = f"Generate a personalized investment plan for a {age}-year-old working as a {profession}. Consider their potential risk tolerance, time horizon, and financial goals. Provide a brief overview of suitable asset classes and investment strategies."

        # Generate content using Gemini API
        response = model.generate_content(prompt)
        generated_text = response.text

        return jsonify({"generated_text": generated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
