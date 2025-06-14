# Import required libraries
from flask import Flask, request, send_file, render_template, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import tempfile
import json
import os
import re
from collections import defaultdict
import math
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert

# Initialize Flask application
app = Flask(__name__, static_folder='static')
CORS(app)

# Helper function to extract text blocks with precise positioning
def extract_text_blocks(page):
    blocks = []
    text_page = page.get_textpage()
    dict_page = text_page.extractDICT()
    
    for block in dict_page["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                if "spans" in line:
                    for span in line["spans"]:
                        # Get comprehensive font information
                        font_info = {
                            "font": span["font"],
                            "size": span["size"],
                            "flags": span["flags"],
                            "color": span["color"],
                            "characteristics": get_font_characteristics(span)
                        }
                        
                        # Calculate precise bounds and transform
                        x0, y0, x1, y1 = span["bbox"]
                        transform = span.get("transform", [1, 0, 0, 1, x0, y0])
                        
                        # Get text metrics
                        metrics = analyze_text_metrics(span)
                        
                        blocks.append({
                            "text": span["text"],
                            "bbox": [x0, y0, x1, y1],
                            "font_info": font_info,
                            "transform": transform,
                            "metrics": metrics,
                            "text_render_mode": span.get("render_mode", 0),
                            "char_spacing": span.get("char_spacing", 0),
                            "word_spacing": span.get("word_spacing", 0)
                        })
    
    return blocks

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Allow requests from different origins (needed for local development)

# Root endpoint - Used to check if server is running
@app.route('/')
def home():
    return render_template('index.html')  # Ensure 'index.html' exists in the templates folder

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
                except ValueError as e:
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

        except (FileNotFoundError, IOError) as e:
            return f'Error processing PDF: {str(e)}', 400

        finally:
            # Clean up temporary files
            if os.path.exists(temp_in_path):
                os.remove(temp_in_path)
            if os.path.exists(temp_out_path):
                os.remove(temp_out_path)

    except (FileNotFoundError, IOError) as e:
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

# Endpoint for editing PDFs
@app.route('/edit-pdf', methods=['POST'])
def edit_pdf():
    if 'pdfFile' not in request.files:
        return 'No file uploaded', 400
    if 'pdfContent' not in request.form:
        return 'No content provided', 400

    pdf_file = request.files['pdfFile']
    new_content = request.form['pdfContent']

    if not pdf_file.filename.lower().endswith('.pdf'):
        return 'Invalid file type. Please upload a PDF file.', 400

    try:
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_in:
            pdf_file.save(temp_in)
            temp_in_path = temp_in.name

        # Open the PDF with PyMuPDF
        doc = fitz.open(temp_in_path)

        # Replace text on the first page (for simplicity)
        if len(doc) > 0:
            page = doc[0]
            page.clean_contents()  # Clean existing content
            rect = fitz.Rect(72, 72, 500, 200)  # Define a rectangle for text placement
            page.insert_textbox(rect, new_content, fontsize=12, color=(0, 0, 0))

        # Save the edited PDF to a temporary file
        temp_out_path = temp_in_path.replace('.pdf', '_edited.pdf')
        doc.save(temp_out_path)
        doc.close()

        return send_file(temp_out_path, as_attachment=True, download_name='edited.pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint for saving edited PDF with enhanced precision
@app.route('/save-pdf-edits', methods=['POST'])
def save_pdf_edits():
    if 'pdfFile' not in request.files or 'edits' not in request.form:
        return jsonify({'error': 'Missing PDF file or edits'}), 400

    pdf_file = request.files['pdfFile']
    edits = json.loads(request.form['edits'])
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_in:
            pdf_file.save(temp_in.name)
            input_path = temp_in.name

        # Open PDF with PyMuPDF
        doc = fitz.open(input_path)
        
        # Group edits by page number
        edits_by_page = defaultdict(list)
        for edit in edits:
            page_num = edit.get('currentPage', 1) - 1 # Adjust to 0-based index
            if 0 <= page_num < len(doc):
                edits_by_page[page_num].append(edit)
            else:
                print(f"Warning: Edit for invalid page number {page_num + 1} ignored.")

        # Process edits for each page
        for page_num, page_edits in edits_by_page.items():
            page = doc[page_num]
            
            # Sort edits by vertical position to avoid clearing text needed for later edits on the same line
            page_edits.sort(key=lambda x: x['originalData']['bbox'][1])

            for edit in page_edits:
                original_data = edit['originalData']
                new_text = edit['text']
                
                # Clear original text area using the original bounding box
                if original_data.get('bbox'):
                    clear_text_area(page, original_data['bbox'])
                
                # Insert new text with original style and position
                if new_text.strip():
                    # Use the original transform matrix for precise positioning
                    transform = original_data.get('transform', [1, 0, 0, 1, original_data.get('bbox', [0,0,0,0])[0], original_data.get('bbox', [0,0,0,0])[1]])
                    font_info = original_data.get('font_info', {})
                    
                    # Extract position from transform matrix (tx, ty)
                    position = (transform[4], transform[5])
                    
                    # Extract rotation from transform matrix
                    rotation = math.degrees(math.atan2(transform[1], transform[0]))

                    insert_text_with_style(
                        page=page,
                        text=new_text,
                        position=position,
                        font_info=font_info,
                        rotation=rotation
                    )

        # Save to new file
        output_path = input_path.replace('.pdf', '_edited.pdf')
        doc.save(output_path)
        doc.close()
        
        # Send edited PDF
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='edited.pdf'
        )
            
    except Exception as e:
        print(f"Error in save_pdf_edits: {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        # Clean up temporary input file
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)
        # Clean up temporary output file if it was created
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)

# Endpoint for PDF to Word conversion
@app.route('/pdf-to-word', methods=['POST'])
def pdf_to_word():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No PDF file uploaded'}), 400
    pdf_file = request.files['pdfFile']
    if not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type'}), 400
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            pdf_file.save(temp_pdf.name)
            docx_path = temp_pdf.name.replace('.pdf', '.docx')
            cv = Converter(temp_pdf.name)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
        return send_file(docx_path, as_attachment=True, download_name=pdf_file.filename.replace('.pdf', '.docx'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'temp_pdf' in locals() and os.path.exists(temp_pdf.name):
            os.remove(temp_pdf.name)
        if 'docx_path' in locals() and os.path.exists(docx_path):
            os.remove(docx_path)

# Endpoint for Word to PDF conversion
@app.route('/word-to-pdf', methods=['POST'])
def word_to_pdf():
    if 'docxFile' not in request.files:
        return jsonify({'error': 'No DOCX file uploaded'}), 400
    docx_file = request.files['docxFile']
    if not docx_file.filename.lower().endswith('.docx'):
        return jsonify({'error': 'Invalid file type'}), 400
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_docx:
            docx_file.save(temp_docx.name)
            pdf_path = temp_docx.name.replace('.docx', '.pdf')
            docx2pdf_convert(temp_docx.name, pdf_path)
        return send_file(pdf_path, as_attachment=True, download_name=docx_file.filename.replace('.docx', '.pdf'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'temp_docx' in locals() and os.path.exists(temp_docx.name):
            os.remove(temp_docx.name)
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.remove(pdf_path)

# Helper function to clear text area more precisely (using white rectangle)
def clear_text_area(page, bbox):
    rect = fitz.Rect(bbox)
    # Draw a white rectangle over the bounding box to clear the text
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))

# Enhanced text insertion with better positioning and style matching
def insert_text_with_style(page, text, position, font_info, rotation=0):
    try:
        # Get font name and size
        font_name = font_info.get('font', 'helv')
        font_size = font_info.get('size', 12)
        
        # Get font color (PyMuPDF uses RGB tuples)
        font_color = font_info.get('color', (0, 0, 0))
        
        # Get font flags for bold/italic
        font_flags = font_info.get('flags', 0)
        
        # Try to insert text with the specified font and style
        # PyMuPDF's insert_text handles positioning based on the 'point' argument
        # and applies rotation based on the 'rotate' argument.
        page.insert_text(
            point=position,
            text=text,
            fontname=font_name,
            fontsize=font_size,
            color=font_color,
            rotate=rotation,
            flags=font_flags
        )
        
        return True
        
    except Exception as e:
        print(f"Error inserting text with style: {str(e)}")
        # Fallback to a default font if the specified font fails
        try:
            page.insert_text(
                point=position,
                text=text,
                fontname='helv', # Fallback font
                fontsize=font_size,
                color=font_color,
                rotate=rotation
            )
            return True
        except Exception as fallback_e:
            print(f"Fallback font insertion failed: {str(fallback_e)}")
            return False

# Helper functions for font and text analysis
def get_font_characteristics(span):
    """Extract detailed font characteristics from a PDF text span."""
    font_name = span["font"].lower()
    font_flags = {
        "bold": bool(span["flags"] & (1 << 18)),
        "italic": bool(span["flags"] & (1 << 19)),
        "monospace": font_name.startswith(("courier", "mono")),
        "serif": any(serif in font_name for serif in ("times", "georgia", "garamond")),
        "script": any(script in font_name for script in ("script", "cursive", "brush"))
    }
    return font_flags

def analyze_text_metrics(span):
    """Analyze text metrics including character spacing and alignment."""
    text = span["text"]
    bbox = span["bbox"]
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    
    metrics = {
        "char_count": len(text),
        "avg_char_width": width / len(text) if text else 0,
        "line_height": height,
        "baseline": bbox[1],
        "alignment": "left"  # Default, could be updated based on block analysis
    }
    
    return metrics

# Endpoint for extracting text with precise positioning
@app.route('/extract-pdf-text', methods=['POST'])
def extract_pdf_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Not a PDF file"}), 400
        
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            
            # Open PDF and extract text from specified page
            doc = fitz.open(temp_file.name)
            page_num = int(request.form.get('page', 1)) - 1
            page = doc[page_num]
            
            # Extract text blocks with enhanced information
            blocks = extract_text_blocks(page)
            
            # Get page dimensions for coordinate normalization
            page_rect = page.rect
            dimensions = {
                "width": page_rect.width,
                "height": page_rect.height
            }
            
            # Clean up
            doc.close()
            os.unlink(temp_file.name)
            
            return jsonify({
                "blocks": blocks,
                "dimensions": dimensions,
                "page_count": len(doc)
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask server when running this file directly
if __name__ == '__main__':
    # Ensure the 'templates' directory exists for render_template
    if not os.path.exists('templates'):
        os.makedirs('templates')
    # You might also need to copy index.html to the templates folder
    # For example: shutil.copy('index.html', 'templates/')
    
    app.run(debug=True)
