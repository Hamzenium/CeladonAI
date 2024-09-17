from flask import Blueprint, request, jsonify
from services.embedding_service import get_embedding, array_embedder
from services.embedding_service import create_prompt, generate_answer
from utils.similarity import cosine_similarity

query_blueprint = Blueprint('query', __name__)

@query_blueprint.route('/query', methods=['POST'])
def query_document():
    data = request.json
    question = data['question']
    document_paragraphs = data['paragraphs']
    
    embeddings = array_embedder(document_paragraphs)
    question_embedding = get_embedding(question)
    
    # Assume cosine_similarity function exists
    best_paragraph = cosine_similarity(question_embedding, embeddings)
    
    prompt = create_prompt(best_paragraph, question)
    answer = generate_answer(prompt)
    
    return jsonify({'answer': answer}), 200
