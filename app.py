import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message: return jsonify({"response": "No message."})
    
    try:
        # BYPASS TRICK: Google Gemini ko hatakar direct jawab likh diya
        ai_response = "Hello Sir. I am J.A.R.V.I.S. My advanced voice module is now fully operational."

        audio_data = ""
        if ELEVENLABS_API_KEY:
            voice_id = "pNInz6obbfdqIcacX1tf" # Adam Voice
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            data = {
                "text": ai_response,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            tts_res = requests.post(url, json=data, headers=headers)
            
            if tts_res.status_code == 200:
                audio_data = base64.b64encode(tts_res.content).decode('utf-8')

        return jsonify({"response": ai_response, "audio": audio_data})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
