from flask import Flask, request, jsonify
from pptx import Presentation
import os

app = Flask(__name__)

@app.route('/scrape_pptx', methods=['POST'])
def scrape_pptx():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    pptx_file = request.files['file']

    # Check if the file is a PowerPoint file
    if pptx_file.filename.endswith('.pptx') or pptx_file.filename.endswith('.PPTX'):
        try:
            # Save the uploaded file in a temporary location
            filepath = os.path.join('/tmp', pptx_file.filename)
            pptx_file.save(filepath)

            # Extract text from the PowerPoint file
            prs = Presentation(filepath)
            extracted_text = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                extracted_text += run.text

            # Remove the temporary file
            print(extracted_text)
            os.remove(filepath)

            return jsonify({'text': extracted_text})

        except Exception as e:
            return jsonify({'error': 'Error occurred while extracting text: {}'.format(str(e))})

    else:
        return jsonify({'error': 'Invalid file format. Only PowerPoint files are supported.'})

if __name__ == '__main__':
    app.run(debug=True)
