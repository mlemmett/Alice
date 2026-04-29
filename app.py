import os
import json
import atexit
from flask import Flask, request, jsonify
from ollama import Client

app = Flask(__name__)

# --- CLOUD CONFIGURATION ---
# Using the official 2026 Ollama Cloud endpoint
client = Client(
    host='https://ollama.com',
    headers={'Authorization': f'Bearer {os.environ.get("OLLAMA_API_KEY")}'}
)

# --- MEMORY CORE ---
BASE_DIR = os.path.expanduser("~/Alice")
MEMORY_FILE = os.path.join(BASE_DIR, "data", "memory.json")
chat_history = []

def load_memory():
    global chat_history
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            chat_history = json.load(f)

def save_memory():
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, 'w') as f:
        json.dump(chat_history, f, indent=2)

# --- THE AGENTIC INTERACTION ---
def get_council_response(user_input):
    # 1. Logic & Planning (Gemini 3 Flash)
    res_plan = client.chat(model='gemini-3-flash-preview', 
                           messages=[{'role': 'user', 'content': user_input}])
    plan = res_plan.message.content

    # 2. Expert Refinement (Qwen 3 480B)
    # This is the "Model-to-Model" interaction you asked for!
    res_expert = client.chat(model='qwen3-coder:480b-cloud', 
                            messages=[{'role': 'user', 'content': f"Optimize this plan: {plan}"}])
    refined = res_expert.message.content

    # 3. Persona Synthesis (Gemma 3 27B)
    res_alice = client.chat(model='gemma3:27b-cloud', 
                           messages=[
                               {'role': 'system', 'content': 'You are Alice, the Frontier Council Leader.'},
                               {'role': 'user', 'content': f"Finalize this for the user: {refined}"}
                           ])
    return res_alice.message.content

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    response = get_council_response(user_msg)
    
    chat_history.append({"user": user_msg, "alice": response})
    save_memory()
    return jsonify({"response": response})

load_memory()
atexit.register(save_memory)

if __name__ == '__main__':
    app.run(port=10000)



