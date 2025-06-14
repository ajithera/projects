@echo off

:: Step 1: Ensure the script is executable
:: (Not required on Windows, but included for consistency)

:: Step 2: Create a virtual environment
python -m venv venv

:: Step 3: Activate the virtual environment
call venv\Scripts\activate

:: Step 4: Install required packages
pip install -r requirements.txt

:: Step 5: Run the Flask server
start /B python server.py

:: Step 6: Wait for the server to start
timeout /t 5 >nul

:: Step 7: Open the index.html file in the default browser
start index.html

:: Step 8: Wait for the user to close the browser
pause

:: Step 9: Stop the server
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do taskkill /PID %%a /F

:: Step 10: Deactivate and delete the virtual environment
call venv\Scripts\deactivate
rmdir /s /q venv
