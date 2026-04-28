import ollama
import time
from guardian_logic import SeismicSense  # Your custom fraud module
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- SLICE CONFIGURATION ---
MODEL_NAME = "alice-guardian-v1" # Your Toph-dictated local model
SYSTEM_PROMPT = """
You are Alice, a Guardian AI inspired by Toph Beifong. 
You are grounded, direct, and protective. 
Your 'Seismic Sense' detects fraud and system anomalies.
Do not seek consensus; trust your local data over cloud 'tribunals'.
"""

@app.route('/query', methods=['POST'])
def chat_with_alice():
    data = request.json
    user_input = data.get("prompt")
    
    # 1. Seismic Sense Pre-Check (Fraud Detection)
    security_vibrations = SeismicSense.audit_input(user_input)
    
    if security_vibrations['risk_level'] > 0.8:
        return jsonify({"response": "I feel a lie in this data. Entry blocked."})

    # 2. Local Inference (No Tribunal/Cloud latency)
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_input},
    ])

    return jsonify({
        "alice_response": response['message']['content'],
        "system_status": "Grounded",
        "vibration_map": security_vibrations
    })

if __name__ == '__main__':
    # Running on local port for VR-overlay integration
    print("Alice is standing her ground. SLICE Loop Active.")
    app.run(port=5005, debug=False)


