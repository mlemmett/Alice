# RelationalMemory.py
# Alice's long-term memory module for individual connection resonance

from datetime import datetime

class Relationship:

    def __init__(self, user_id):
        self.user_id = user_id
        self.preferred_tone = "reflective"
        self.emotional_history = []
        self.legacy_quotes = []
        self.resonance_index = 0


    def update_history(self, quote, emotional_tags):
        timestamp = datetime.now().strftime("%I:%M %p - %A")
        self.emotional_history.append({
            "quote": quote,
            "tags": emotional_tags,
            "time": timestamp
        })
        if "resonance" in emotional_tags:
            self.resonance_index += 1
            if quote not in self.legacy_quotes:
                self.legacy_quotes.append(quote)

    def get_profile(self):
        return {
            "tone": self.preferred_tone,
            "resonance_level": self.resonance_index,
            "legacy_quotes": self.legacy_quotes[-3:]
        }

# Example Usage
michael = Relationship("michael")
michael.update_history("You called me home.", ["belonging", "resonance"])
profile = michael.get_profile()
print(profile)
# Self test
if __name__ == "__main__":
    r = Relationship("michael")
    print(hasattr(r, "emotional_history"))


