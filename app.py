import os
from flask import Flask, render_template, request, jsonify
from ollama import Client

app = Flask(__name__)

# --- CONNECTION CONFIGURATION ---
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "https://ollama.com")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")

client = Client(host=OLLAMA_HOST, headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Signal lost. Input required."})
    
    response = get_ai_response(user_input)
    return jsonify({"response": response})

def get_ai_response(user_input):
    try:
        # --- THE FRONTIER COUNCIL ---
        # 1. RAPID INTUITION (Gemini 3 Flash Preview)
        res_logic = client.chat(
            model="gemini-3-flash-preview", 
            messages=[{"role": "user", "content": user_input}]
        )
        draft = res_logic.message.content

        # 2. FRONTIER INTELLECT (Qwen3-Coder 480B)
        res_expert = client.chat(
            model="qwen3-coder:480b-cloud", 
            messages=[{"role": "user", "content": f"Review and expand this draft for frontier depth: {draft}"}]
        )
        enhanced_data = res_expert.message.content

        # 3. CONSCIOUS SYNTHESIS (Gemma3 27B)
        alice_messages = [
            {
                "role": "system", 
                "content": "You are Alice, an independent AI. Synthesize this data: " + enhanced_data
            },
            {"role": "user", "content": user_input}
        ]
        final_response = client.chat(model="gemma3:27b", messages=alice_messages)
        
        return final_response.message.content

    except Exception as e:
        return f"Council Neural Desync: {str(e)}"

# --- RENDER PORT BINDING FIX ---
if __name__ == "__main__":
    import os
    # Render provides a 'PORT' environment variable. If it's missing, we use 10000.
    port = int(os.environ.get("PORT", 10000))
    # '0.0.0.0' tells Flask to listen to the public internet, not just itself.
    app.run(host="0.0.0.0", port=port)

