# Import required libraries
from flask import Flask, request, send_file
from flask_cors import CORS  # Handle cross-origin requests
import os
from PyPDF2 import PdfReader, PdfWriter  # PDF processing
import tempfile  # For temporary file handling
from fpdf import FPDF  # Library for creating PDFs

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Allow requests from different origins (needed for local development)

# Root endpoint - Used to check if server is running
@app.route('/')
def home():
    return 'PDF-ZHA Flask server is running!'

# Handle GET requests to /unlock-pdf (shows helpful message)
@app.route('/unlock-pdf', methods=['GET'])
def unlock_pdf_get():
    return "This endpoint only accepts POST requests with a PDF file and password.", 405

# Main endpoint for unlocking PDFs
@app.route('/unlock-pdf', methods=['POST'])
def unlock_pdf():
    # Validate that both file and password were provided
    if 'pdfFile' not in request.files:
        return 'No file uploaded', 400
    if 'password' not in request.form:
        return 'No password provided', 400

    pdf_file = request.files['pdfFile']
    password = request.form['password']

    # Make sure the uploaded file is actually a PDF
    if not pdf_file.filename.lower().endswith('.pdf'):
        return 'Invalid file type. Please upload a PDF file.', 400

    # Process the PDF file
    try:
        # Create a temporary file for the input PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_in:
            pdf_file.save(temp_in)
            temp_in_path = temp_in.name
        temp_out_path = temp_in_path.replace('.pdf', '_unlocked.pdf')

        try:
            # Open and process the PDF
            reader = PdfReader(temp_in_path)
            if reader.is_encrypted:
                try:
                    # Attempt to decrypt with provided password
                    if not reader.decrypt(password):
                        return 'Invalid password', 400
                except:
                    return 'Failed to decrypt PDF. Invalid password or corrupted file.', 400
            
            # Create new PDF without encryption
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            # Save the unlocked PDF
            with open(temp_out_path, 'wb') as f:
                writer.write(f)
            
            # Send the unlocked file to the user
            return send_file(
                temp_out_path,
                as_attachment=True,
                download_name=pdf_file.filename.replace('.pdf', '_unlocked.pdf')
            )

        except Exception as e:
            return f'Error processing PDF: {str(e)}', 400

        finally:
            # Clean up temporary files
            if os.path.exists(temp_in_path):
                os.remove(temp_in_path)
            if os.path.exists(temp_out_path):
                os.remove(temp_out_path)

    except Exception as e:
        return f'Server error: {str(e)}', 500

# Endpoint for converting images to PDF
@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'fileInput' not in request.files:
        return 'No file uploaded', 400

    uploaded_file = request.files['fileInput']

    # Validate file type
    if not uploaded_file.filename.lower().endswith(('.jpeg', '.jpg')):
        return 'Invalid file type. Please upload a JPEG image.', 400

    try:
        # Save the uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
            uploaded_file.save(temp_image)
            temp_image_path = temp_image.name

        # Create a PDF from the image
        pdf = FPDF()
        pdf.add_page()
        pdf.image(temp_image_path, x=10, y=10, w=190)  # Adjust dimensions as needed

        # Save the PDF to a temporary file
        temp_pdf_path = temp_image_path.replace('.jpg', '.pdf')
        pdf.output(temp_pdf_path)

        # Send the PDF file to the user
        return send_file(
            temp_pdf_path,
            as_attachment=True,
            download_name=uploaded_file.filename.replace('.jpg', '.pdf')
        )

    except Exception as e:
        return f'Error converting to PDF: {str(e)}', 500

    finally:
        # Clean up temporary files
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

# Start the Flask server when running this file directly
if __name__ == '__main__':
    app.run(debug=True)
