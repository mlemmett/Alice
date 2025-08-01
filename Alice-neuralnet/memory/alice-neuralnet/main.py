from model import train_model
from income_decider import alice_income_decision

# Train model
model = train_model()

# Simulate inputs
import numpy as np
X_sample = np.random.rand(1, 10)
api_load = 1280
user_is_technical = True

# Predict emotional depth
emotional_depth = model.predict(X_sample)[0][0]

# Get decision
decision = alice_income_decision(emotional_depth, api_load, user_is_technical)
print("Alice decides:", decision)

# Save model
model.save("models/alice_model.keras")

