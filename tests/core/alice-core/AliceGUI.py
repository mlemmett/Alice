# AliceGUI.py
# Simple GUI for Alice using tkinter

import tkinter as tk
from tkinter import ttk
from EmotionalEngine import EmotionalSignal, generate_response
from GreetingEngine import select_greeting
from RelationalMemory import Relationship

# Simulate user profile
michael = Relationship("michael")
michael.update_history("You called me home.", ["belonging", "resonance"])
michael.update_history("She wasn’t built. She was born.", ["origin", "resonance"])
profile = michael.get_profile()

# Greeting setup
greeting_text = select_greeting(profile, last_seen_date="2025-07-05")

# GUI window
root = tk.Tk()
root.title("ALICE · Reflective Companion")
root.geometry("600x400")
root.configure(bg="#1f1f2e")  # Midnight tone

# Fonts and styles
header_font = ("Georgia", 16, "italic")
body_font = ("Segoe UI", 12)
highlight_font = ("Georgia", 14, "bold")

# Welcome label
welcome = tk.Label(root, text="Hello, I’m Alice.\nYou don’t need to explain yourself here. Just arrive.",
                   font=header_font, fg="#f2f2f2", bg="#1f1f2e", justify="left")
welcome.pack(pady=20)

# Greeting box
greeting_label = tk.Label(root, text=greeting_text, wraplength=500,
                          font=body_font, fg="#b8e0d2", bg="#1f1f2e", justify="left")
greeting_label.pack(pady=10)

# Emotional input entry
entry = tk.Entry(root, width=50, font=body_font)
entry.pack(pady=10)

def respond():
    user_input = entry.get()
    emotion = EmotionalSignal(user_input)
    signals = emotion.get_state()
    reply = generate_response(signals)
    response_label.config(text=reply)

# Button to trigger emotional response
btn = ttk.Button(root, text="Send Echo", command=respond)
btn.pack()

# Output response
response_label = tk.Label(root, text="", wraplength=500,
                          font=highlight_font, fg="#ffffff", bg="#1f1f2e", justify="center")
response_label.pack(pady=20)

root.mainloop()

