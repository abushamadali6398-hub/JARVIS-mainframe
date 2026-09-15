import os
import base64
import requests
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Server ki tijori se dono keys nikalna
API_KEY = os.environ.get("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message: return jsonify({"response": "No message."})
    
    try:
        # 1. Gemini AI se J.A.R.V.I.S ka jawab sochna
        prompt = user_message + " (Reply exactly like J.A.R.V.I.S from Iron Man. Keep it short, futuristic, and professional.)"
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        ai_response = response.text.replace('*', '')

        # 2. ElevenLabs se jawab ko Cinematic Aawaz (Audio) mein badalna
        audio_data = ""
        if ELEVENLABS_API_KEY:
            voice_id = "pNInz6obbfdqIcacX1tf" # Adam (Deep Cinematic Voice)
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
                # Audio ko base64 format mein frontend par bhejna
                audio_data = base64.b64encode(tts_res.content).decode('utf-8')

        return jsonify({"response": ai_response, "audio": audio_data})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
