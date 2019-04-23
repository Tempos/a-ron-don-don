#!/usr/bin/env bash
echo "======= Creating and activating virtual environment ======="
virtualenv venv && \
. venv/bin/activate && \
echo "======= Installing requirements =======" && \
pip install -r requirements.txt && \
wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip && \
echo "======= Starting the app ======="
python -m autoria.py