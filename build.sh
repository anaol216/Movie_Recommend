#!/bin/bash

# Install dependencies
pip install -r requirements.txt
pip install kaggle

# Setup Kaggle API key
mkdir -p ~/.kaggle
echo "$KAGGLE_JSON" > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
kaggle datasets download -d arashnic/an-unbiased-sequential-recommendation-dataset

# Unzip the dataset
unzip an-unbiased-sequential-recommendation-dataset.zip -d data

# Run your notebook script
python main.py
