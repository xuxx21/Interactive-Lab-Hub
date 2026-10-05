#!/bin/bash

# Ask the question using Piper TTS
echo "What time is it right now?" | python3 -m piper \
  -m en_US-lessac-medium \
  --output-raw | aplay -r 22050 -f S16_LE -t raw -

# Give the respondent a moment to prepare
sleep 1

echo "Listening..."

# Record the numerical answer
arecord -d 5 -f cd -c 1 -r 16000 time_answer.wav

echo "Recording complete."

# Transcribe the answer
python transcribe.py time_answer.wav --model base.en

