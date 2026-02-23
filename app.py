from flask import Flask, request, jsonify
import uuid, json, os, datetime

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

