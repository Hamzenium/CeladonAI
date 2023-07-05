from flask import Flask, request, jsonify
from pptx import Presentation
import openai
import os

app = Flask(__name__)
openai.api_key = "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"


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def array_embedder(sub_paragraphs):
    embeddings = []
    for paragraph in sub_paragraphs:
        embeddings.append(get_embedding(paragraph))
    return embeddings

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
            paragraphs = []
            max_words = 200
            words = extracted_text.split()
            while words:
                paragraph = " ".join(words[:max_words])
                paragraphs.append(paragraph)
                words = words[max_words:]
         
            embeddings = array_embedder(paragraphs)
            os.remove(filepath)
            return jsonify({'embeddings': embeddings})

        except Exception as e:
            return jsonify({'error': 'Error occurred while extracting text: {}'.format(str(e))})

    else:
        return jsonify({'error': 'Invalid file format. Only PowerPoint files are supported.'})

if __name__ == '__main__':
    app.run(debug=True)
