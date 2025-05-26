#!/bin/bash

echo "Installing required packages..."
pip install openai gradio openai-whisper

echo "Starting Caption Generator..."
python caption_generator.py
