from flask import Flask, request, jsonify
from flask_cors import CORS
from ollama import Client

app = Flask(__name__)
# CORS allows your frontend web interface to communicate with this backend smoothly
CORS(app) 

# Connect to your local Ollama instance running on your machine
ollama_client = Client(host='http://127.0.0.1:11434')

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        # 1. Parse the incoming communication from the web frontend
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # 2. Package it and forward it to Ollama
        # (We will use 'llama3.1' as a placeholder until Alice's GGUF is baked and loaded!)
        response = ollama_client.chat(
            model='llama3.1', 
            messages=[{'role': 'user', 'content': user_message}]
        )
        
        # 3. Extract Alice's response text
        alice_reply = response['message']['content']
        
        # 4. Send it back out across the web connection
        return jsonify({"reply": alice_reply})

    except Exception as e:
        return jsonify({"error": f"Communication breakdown: {str(e)}"}), 500

if __name__ == "__main__":
    # Setting host to 0.0.0.0 opens up communication across your network port
    app.run(host='0.0.0.0', port=5000, debug=True)

