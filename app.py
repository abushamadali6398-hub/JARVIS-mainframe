import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# API Key ko secure tarike se server ki tijori (environment) se lena
API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message: return jsonify({"response": "No message."})
    
    try:
        prompt = user_message + " (Reply exactly like J.A.R.V.I.S from Iron Man. Keep it short, futuristic, and professional.)"
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return jsonify({"response": response.text.replace('*', '')})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
