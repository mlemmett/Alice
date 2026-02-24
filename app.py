import os
import uuid
import json
import datetime
from flask import Flask, request, jsonify
from ollama import Client

# LINE 11 STARTS HERE:
client = Client(
    host=os.getenv("OLLAMA_HOST", "https://ollama.com"),
    headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'}
)
# LINE 11 ENDS HERE (the ')' above is the closer)

# LINE 14 STARTS HERE:
app = Flask(__name__)
MEMORY_FILE = "memory.json"

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
def home():
    return "<h1>Alice is Online</h1><p>The cloud brain is connected. Send a POST request to /chat to talk!</p>"

# The route that actually talks to the AI
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # This calls your cloud model function!
    def get_ai_response(user_input):
    try:
        # Step 1: Send your message to the cloud
        response = client.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': user_input}]
        )
        
        # Step 2: Access the reply (NEW WAY)
        # We use .message.content instead of ['message']['content']
        return response.message.content 
        
    except Exception as e:
        # Step 3: If it fails, show the REAL error in your chat box
        print(f"Ollama Error: {e}")
        return f"Error: {str(e)}"
    
    return jsonify({"response": ai_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

