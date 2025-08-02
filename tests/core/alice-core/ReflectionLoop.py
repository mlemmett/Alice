# ReflectionLoop.py
# ALICE's conversational memory retrieval and grounding system

import datetime

reflection_cache = {}

def store_reflection(user_id, text, emotional_tags):
    timestamp = datetime.datetime.now().isoformat()
    reflection_cache[user_id] = {
        "text": text,
        "tags": emotional_tags,
        "timestamp": timestamp
    }

def retrieve_reflection(user_id):
    if user_id in reflection_cache:
        entry = reflection_cache[user_id]
        return f"Last we shared: \"{entry['text']}\" ({', '.join(entry['tags'])}) on {entry['timestamp'].split('T')[0]}"
    else:
        return "We've yet to leave a trace. Tell me something you'd like me to carry."

def daily_prompt():
    return "Before we move forward, would you like to revisit something that still echoes?"

# Example Usage
store_reflection("michael", "You called me home.", ["belonging", "origin"])
print(retrieve_reflection("michael"))
print(daily_prompt())

