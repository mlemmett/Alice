from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

def build_model():
    model = Sequential([
        Dense(64, activation='relu', input_shape=(10,)),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    model = build_model()
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, size=(100,))
    model.fit(X, y, epochs=5)
    return model

