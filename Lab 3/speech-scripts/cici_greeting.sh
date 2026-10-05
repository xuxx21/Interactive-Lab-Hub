#!/bin/bash


echo "Hi Cici! Welcome back. It's nice to see you again!" | python3 -m piper -m en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -

