import os
import uuid
import json
import datetime
from flask import Flask, request, jsonify
from ollama import Client

client = Client(
    host=os.getenv("OLLAMA_HOST", "https://ollama.com"),
    headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'}
)

# LINE 14 STARTS HERE:
from flask import Flask, render_template
import threading
import requests
import time



app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def neural_interface():
    if request.method == 'POST':
        # This pulls the 'message' you typed on your phone
        data = request.get_json()
        user_text = data.get('message', '')
        
        # This is where we create the reply
        reply_text = f"ALICE: Analysis complete. You said: '{user_text}'"
       
        return jsonify({"reply": reply_text})
    return render_template('index.html')
MODEL_NAME = "qwen3-coder:480b-cloud"
MEMORY_FILE = "memory.json"
# 1. The 'Self-Ping' Route: Lightweight and fast
@app.route('/heartbeat')
def heartbeat():
    return "Heartbeat received", 200

# 2. The Background Worker: Pings the app every 12 minutes
def keep_alive():
    # FIX: Corrected URL with proper quotes
    url = "https://alice-lb3p.onrender.com/heartbeat"
    while True:
        try:
            requests.get(url)
        except:
            # Silently handle connection errors
            pass
        time.sleep(720) 

# FIX: Start the background thread so it actually runs
threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    # Ensure Alice listens on the port Render expects
    app.run(host="0.0.0.0", port=10000)
# Load or initialize memory file
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/memory/store", methods=["POST"])
def store_memory():
    data = request.json or {}

    # Apply governance rules
    allowed, message = apply_governance(data)
    if not allowed:
        return jsonify({"status": message}), 400

    # Build the memory object
    memory = {
        "id": str(uuid.uuid4()),
        "type": data.get("type", "episodic"),
        "content": data.get("content", ""),
        "tags": data.get("tags", []),
        "importance": data.get("importance", 0.5),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # Load, append, save
    all_memory = load_memory()
    all_memory.append(memory)
    save_memory(all_memory)

    return jsonify({"status": "stored", "id": memory["id"]})


@app.route("/memory/query", methods=["POST"])
def query_memory():
    query = request.json
    mem = load_memory()
    results = []

    for m in mem:
        if query.get("type") and m["type"] != query["type"]:
            continue
        if query.get("tags"):
            if not any(tag in m["tags"] for tag in query["tags"]):
                continue
        if query.get("keyword") and query["keyword"] not in m["content"]:
            continue
        if query.get("min_importance") and m["importance"] < query["min_importance"]:
            continue
        results.append(m)

    return jsonify({"results": results})

@app.route("/memory/delete", methods=["DELETE"])
def delete_memory():
    mem_id = request.json.get("id")
    mem = load_memory()
    mem = [m for m in mem if m["id"] != mem_id]
    save_memory(mem)
    return jsonify({"status": "deleted"})

# The "Home" page you see in the browser
@app.route('/')
@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Alice AI</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: #00ffcc; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                #chat-container { width: 90%; max-width: 600px; background: #1a1a1a; border-radius: 15px; padding: 20px; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2); }
                #chat-box { height: 400px; overflow-y: auto; margin-bottom: 20px; border-bottom: 1px solid #333; padding: 10px; }
                .input-group { display: flex; gap: 10px; }
                input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #333; background: #222; color: white; outline: none; }
                button { padding: 12px 24px; border-radius: 8px; border: none; background: #00ffcc; color: #000; font-weight: bold; cursor: pointer; transition: 0.3s; }
                button:hover { background: #00cca3; }
                .msg { margin-bottom: 15px; line-height: 1.4; }
                .user-msg { color: #888; }
            </style>
        </head>
        <body>
            <div id="chat-container">
                <h2 style="text-align: center;">Alice Neural Interface</h2>
                <div id="chat-box"></div>
                <div class="input-group">
                    <input type="text" id="user-input" placeholder="Initiate communication..." onkeypress="if(event.key==='Enter') sendMessage()">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
            <script>
                async function sendMessage() {
                    const input = document.getElementById('user-input');
                    const box = document.getElementById('chat-box');
                    if (!input.value.trim()) return;

                    const userText = input.value;
                    box.innerHTML += `<div class="msg user-msg"><b>User:</b> ${userText}</div>`;
                    input.value = 'Processing...';
                    input.disabled = true;

                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: userText })
                    });
                    const data = await response.json();
                    box.innerHTML += `<div class="msg"><b>Alice:</b> ${data.response}</div>`;
                    
                    input.value = '';
                    input.disabled = false;
                    input.focus();
                    box.scrollTop = box.scrollHeight;
                }
            </script>
        </body>
    </html>
    """

# --- THE BRIDGE: Receives your text from the website ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # This calls the "Brain" function below
    ai_text = get_ai_response(user_message)
    
    # This sends Alice's final answer back to the screen
    return jsonify({"response": ai_text})

# --- THE BRAIN: Talks to the cloud model ---
def get_ai_response(user_input):
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': user_input}]
        )
        return response.message.content 
    except Exception as e:
        print(f"Ollama Error: {e}")
        return f"Brain Snag: {str(e)}"

# --- THE POWER SWITCH: Keeps the server alive ---
if __name__ == "__main__":
    # Ensure port uses Render's environment variable
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

