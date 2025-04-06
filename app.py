from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS  

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
CORS(app) 

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-pro')  

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

        # Create the prompt
        prompt = (
            f"Generate a personalized investment plan for a {age}-year-old working as a {profession} in India. "
            "Consider India's taxation policies, inflation, government schemes, and investment options. "
            "Suggest asset allocations including mutual funds, fixed deposits, PPF, NPS, gold, real estate, and stock market investments. "
            "Factor in risk tolerance, investment horizon, and financial goals. "
            "Give a structured breakdown with key recommendations for wealth creation and financial security."
        )

        # Generate content using the Gemini model
        response = model.generate_content(prompt)
        generated_text = response.text

        return jsonify({"generated_text": generated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
