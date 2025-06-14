@echo off

:: Step 1: Create a virtual environment
python -m venv venv

:: Step 2: Activate the virtual environment
call venv\Scripts\activate

:: Step 3: Install required packages
pip install -r requirements.txt

:: Step 4: Run the Flask server
start /B python server.py

:: Step 5: Wait for the server to start
timeout /t 5 >nul

:: Step 6: Open the application in the default browser
start http://127.0.0.1:5000

:: Step 7: Wait for the user to close the browser
pause

:: Step 8: Stop the server
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do taskkill /PID %%a /F

:: Step 9: Deactivate and delete the virtual environment
call venv\Scripts\deactivate
rmdir /s /q venv
