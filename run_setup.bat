@echo off
REM --- 1. Start Docker containers ---
echo Starting Docker containers...
docker-compose up -d

REM --- Wait for DB to be ready (10 seconds) ---
timeout /t 10

REM --- 2. Create and activate Python virtual environment ---
echo Creating and activating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM --- 3. Install Python dependencies ---
echo Installing Python dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

REM --- 4. Run the Streamlit application ---
echo Running the Streamlit app...
streamlit run app.py

REM --- Deactivate virtual environment ---
deactivate
