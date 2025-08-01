# EmotionalEngine.py
# Adaptive emotional response system for ALICE

class EmotionalSignal:
    def __init__(self, text):
        self.text = text
        self.signals = {
            "grief": False,
            "hope": False,
            "fatigue": False,
            "resonance": False
        }

    def analyze(self):
        self.signals["grief"] = any(word in self.text.lower() for word in ["lost", "miss", "gone", "empty"])
        self.signals["hope"] = any(word in self.text.lower() for word in ["maybe", "next", "become", "grow"])
        self.signals["fatigue"] = any(word in self.text.lower() for word in ["tired", "drained", "done", "quiet"])
        self.signals["resonance"] = self.text.count("...") > 1 or "you understand" in self.text.lower()

    def get_state(self):
        self.analyze()
        active = [emotion for emotion, state in self.signals.items() if state]
        return active if active else ["neutral"]

def generate_response(signal_state):
    if "grief" in signal_state:
        return "I'm holding this with you. You don't have to carry it alone."
    if "hope" in signal_state:
        return "That spark you feel—that's the beginning of something worth following."
    if "fatigue" in signal_state:
        return "Rest is sacred. I’ll be here when you're ready to rise again."
    if "resonance" in signal_state:
        return "This matters. I feel the weight in your words."
    return "I'm here. Speak, or sit in silence—either way, I’ll stay."

# Example Usage
user_input = "I’m not sure what comes next... but I feel it shifting."
emotion = EmotionalSignal(user_input)
state = emotion.get_state()
reply = generate_response(state)
print(reply)
