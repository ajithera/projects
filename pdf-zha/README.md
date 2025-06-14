# PDF-ZHA Project

PDF-ZHA is a simple web application that allows users to unlock protected PDF files and convert Word or JPEG files to PDF format. The application features a clean and minimalistic user interface, making it easy for users to navigate and utilize its functionalities.

## Features

1. **Unlock Protected PDF Files**: Users can upload a password-protected PDF file and enter the password to unlock it. The unlocked file will be available for download with '_unlocked' appended to the original file name.

2. **Convert Files to PDF**: Users can upload Word documents or JPEG images, which will be converted to PDF format. Once the conversion is complete, the PDF file will be available for download.

## Project Structure

```
pdf-zha
├── index.html          # Main entry point of the website
├── css
│   └── style.css      # Styles for the website
├── js
│   └── script.js      # JavaScript for handling user interactions
├── features
│   ├── unlock-pdf.html # Interface for unlocking PDF files
│   └── convert-to-pdf.html # Interface for converting files to PDF
├── README.md          # Project documentation
```

## Setup Instructions

1. Clone the repository to your local machine.
2. Open the `index.html` file in a web browser to access the application.
3. Follow the on-screen instructions to use the features.

## Running the Server

To run the Flask server for backend functionality, follow these steps:

1. **Navigate to the project directory**:
   Open your terminal and navigate to the project directory where the `pdf-zha` folder is located.
   ```bash
   cd /path/to/your/project/pdf-zha
   ```

2. **Activate the virtual environment**:
   Ensure you have a Python virtual environment set up. Activate it using the following command:
   ```bash
   source venv/bin/activate
   ```
   > **Note**: If you don't have a virtual environment, create one using:
   > ```bash
   > python -m venv venv
   > ```
   > Then activate it as shown above.

3. **Install dependencies**:
   Install the required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask server**:
   Run the following command to start the server:
   ```bash
   python server.py
   ```

5. **Access the application**:
   Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```
   You can now use the web application with backend features enabled.

6. **Stop the server**:
   To stop the server, press `Ctrl+C` in the terminal where the server is running.

> **Tip**: Keep the terminal open while the server is running to see logs and debug information.

## Step-by-Step Instructions to Run the Application

This guide is designed for users with no prior technical knowledge. Follow these steps exactly as written to set up and run the application.

### 1. Install Python
Make sure Python is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

- **Windows**: Download and run the installer. During installation, check the box that says "Add Python to PATH."
- **macOS/Linux**: Python is usually pre-installed. To check, open a terminal and type:
  ```bash
  python3 --version
  ```
  If Python is not installed, download it from the link above.

### 2. Install a Code Editor (Optional)
We recommend using [Visual Studio Code](https://code.visualstudio.com/) to view and edit the project files.

### 3. Download the Project Files
1. Click the green "Code" button on the GitHub repository page.
2. Select "Download ZIP."
3. Extract the ZIP file to a folder on your computer.

### 4. Open a Terminal
- **Windows**: Press `Win + R`, type `cmd`, and press Enter.
- **macOS/Linux**: Open the Terminal application.

### 5. Navigate to the Project Directory
In the terminal, navigate to the folder where you extracted the project files. For example:
```bash
cd /path/to/your/project/pdf-zha
```
Replace `/path/to/your/project` with the actual path to the folder.

### 6. Set Up a Virtual Environment
A virtual environment keeps the project dependencies separate from your system Python.
```bash
python3 -m venv venv
```
Activate the virtual environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 7. Install Required Libraries
Install the necessary Python libraries for the project:
```bash
pip install -r requirements.txt
```

### 8. Start the Flask Server
Run the following command to start the server:
```bash
python server.py
```
You should see output indicating that the server is running at `http://127.0.0.1:5000`.

### 9. Open the Application in a Browser
Open your web browser and go to:
```
http://127.0.0.1:5000
```
You can now use the application to unlock PDFs or convert files to PDF format.

### 10. Stop the Server
To stop the server, go back to the terminal where it is running and press `Ctrl+C`.

### Troubleshooting
- If you encounter any errors, ensure you followed each step exactly.
- For additional help, contact us at:
  - **Email**: ajithkumarjayakumarm@gmail.com
  - **LinkedIn**: [mjajithkumar](https://linkedin.com/in/mjajithkumar)

## License

This project is open-source and available for modification and distribution.