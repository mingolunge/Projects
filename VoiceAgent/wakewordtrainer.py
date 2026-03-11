import openwakeword.data as oww_data
from openwakeword.model import Model
import os

# 1. Define your word
wakeword = "Beemo"

# 2. Generate the synthetic data & Train
# This will take ~45-60 mins depending on your CPU/GPU
# It creates thousands of variations of "Hey Milo" automatically
from openwakeword.training import train_model

train_model(
    target_phrase=wakeword,
    output_dir="my_models",
    steps=10000,           # Increase to 50000 for better accuracy
    batch_size=128,
    patience=20            # Stops training early if it stops improving
)
