#!/bin/bash
set -e

# Generate the Iris dataset
python generate_iris.py

# Start the training process
python model_training.py
