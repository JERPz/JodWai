#!/bin/bash

# --- 1. Start Docker containers ---
echo "Starting Docker containers..."
docker-compose up -d

# --- Wait for DB to be ready ---
echo "Waiting 10 seconds for database to initialize..."
sleep 10

# --- 2. Create and activate Python virtual environment ---
echo "Creating and activating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# --- 3. Install Python dependencies ---
echo "Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# --- 4. Run the Streamlit application ---
echo "Running the Streamlit app..."
streamlit run app.py

# --- Deactivate virtual environment ---
deactivate
