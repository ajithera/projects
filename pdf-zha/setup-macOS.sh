#!/bin/bash

# Step 1: Create a virtual environment
python3 -m venv venv

# Step 2: Activate the virtual environment
source venv/bin/activate

# Step 3: Install required packages
pip install -r requirements.txt

# Step 4: Run the Flask server
python server.py &

# Step 5: Wait for the server to start
sleep 5

# Step 6: Open the application in the default browser
open http://127.0.0.1:5000

SERVER_PID=$!

# Step 7: Wait for the user to close the browser
read -p "Press [Enter] once you have closed the browser to stop the server and clean up."

# Step 8: Stop the server
kill $SERVER_PID

# Step 9: Deactivate and delete the virtual environment
deactivate
rm -rf venv
