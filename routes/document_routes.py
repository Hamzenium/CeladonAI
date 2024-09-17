from flask import Blueprint, request, jsonify
import uuid
from services.document_service import extract_text_from_pdf, extract_text_from_pptx, split_text_into_paragraphs
from services.embedding_service import array_embedder
from services.db_service import save_to_firebase

document_blueprint = Blueprint('documents', __name__)

@document_blueprint.route('/upload/<field>', methods=['POST'])
def scrape_document(field):
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    email = field

    if file.filename.lower().endswith(('.pptx', '.ppt')):
        extracted_text = extract_text_from_pptx(file)
    elif file.filename.lower().endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file)
    else:
        return jsonify({'error': 'Invalid file format'}), 400

    paragraphs = split_text_into_paragraphs(extracted_text)
    embeddings = array_embedder(paragraphs)
    
    save_to_firebase({
        'Paragraphs': paragraphs,
        'embeddings': embeddings
    }, email, str(uuid.uuid4()), file.filename, "link_placeholder")

    return jsonify({'message': 'Document processed successfully'}), 200

