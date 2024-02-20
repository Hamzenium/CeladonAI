from flask import Flask, request, jsonify, session
from flask_session import Session
from pptx import Presentation
import numpy as np
import json
import time
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
import tempfile
import asyncio
import uuid 
import firebase_admin   
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import firestore, storage
from io import BytesIO  # Import BytesIO
from pdfminer.high_level import extract_text
from flask_cors import CORS
cred = credentials.Certificate("key.json")  

firebase_admin.initialize_app(cred, {  "storageBucket": "gs://celadonai-69915.appspot.com"})

db = firestore.client()
user_ref = db.collection('users')
bucket = storage.bucket("celadonai-69915.appspot.com")



app = Flask(__name__)
CORS(app)
openai.api_key = "sk-0tsxXxXpqVdU7Mom2BFOT3BlbkFJzqv7WcNkFfGKbdvtnEyY"


#This function uses the ADA LLM to produce the embeddings of the chunks.
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


#This function is used to break the scraped text into the chunks, and is used as a helper funtion.r
def array_embedder(sub_paragraphs):
    embeddings = []
    for paragraph in sub_paragraphs:
        embeddings.append(get_embedding(paragraph))
    return embeddings



# This end-point was developed to scrape the text from the ppt and store in chunks on firebase.
from flask import request

@app.route('/upload/<field>', methods=['POST'])
def scrape_document(field):
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    email = field
    link = "www.link.com"

    if file.filename.lower().endswith(('.pptx', '.ppt')):
        try:
            extracted_text = extract_text_from_pptx(file)
            document_type = 'pptx'
        except Exception as e:
            return jsonify({'error': f'Error occurred while extracting text from PowerPoint file: {str(e)}'}), 500

    elif file.filename.lower().endswith(('.pdf')):
        try:
            extracted_text = extract_text_from_pdf(file)
            document_type = 'pdf'
        except Exception as e:
            return jsonify({'error': f'Error occurred while extracting text from PDF file: {str(e)}'}), 500

    else:
        return jsonify({'error': 'Invalid file format. Only PowerPoint (PPTX/PPT) and PDF files are supported.'}), 400

    try:
        paragraphs = split_text_into_paragraphs(extracted_text)
        embeddings = array_embedder(paragraphs)
        document_name = file.filename

        # Save the extracted data to Firebase Storage
        document_id = str(uuid.uuid4())
        embeddings_json = json.dumps(embeddings)

        data = {
            'embeddings': embeddings_json,
            'Paragraphs': paragraphs,
            'name': document_name,
            'document_id': document_id,
            f'{document_type}_url': link  # Assuming you want to save the document link as well
        }

        save_to_firebase(data, email, document_id, document_name, link)

        return jsonify({'embeddings': embeddings, 'Paragraphs': paragraphs, 'name': document_name,
                        'id': document_id, f'{document_type}_url': link})

    except Exception as e:
        return jsonify({'error': f'Error occurred while processing document: {str(e)}'}), 500


def extract_text_from_pptx(pptx_file):
    pptx_buffer = BytesIO()
    pptx_file.save(pptx_buffer)
    pptx_buffer.seek(0)
    file_content = pptx_buffer.read()
    prs = Presentation(BytesIO(file_content))
    extracted_text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        extracted_text += run.text
    pptx_buffer.close()
    return extracted_text


def extract_text_from_pdf(pdf_file):
    filepath = os.path.join('/tmp', pdf_file.filename)
    pdf_file.save(filepath)
    text = extract_text(filepath)  # Assuming you have a function to extract text from PDF
    os.remove(filepath)
    return text


def split_text_into_paragraphs(text):
    paragraphs = []
    max_words = 400
    words = text.split()
    while words:
        paragraph = " ".join(words[:max_words])
        paragraphs.append(paragraph)
        words = words[max_words:]
    return paragraphs


def save_to_firebase(data, email, document_id, document_name, link):

    db.collection('users').document(document_id).set(data)
    user_ref = db.collection('email').document(email)
    user_data = user_ref.get()

    if not user_data.exists:
        return jsonify({"error": "User not found"}), 404

    existing_files = user_data.to_dict().get("files", [])
    if not isinstance(existing_files, list):
        existing_files = []

    new_data = {
        'document_id': document_id,
        'document_name': document_name,
        'link': link
    }
    existing_files.append(new_data)

    user_ref.update({
        "files": existing_files
    })



def create_prompt(context, query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Please come up with another question'\n"
    final = header + context + "\n\n" + query + "\n"
    return final 


def generate_answer(prompt, temperature):
    res = openai.Completion.create(
    engine='gpt-3.5-turbo-instruct',
    prompt= prompt,
    temperature=0,
    max_tokens=400,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)
    return res['choices'][0]['text'].strip()


#This end-point was developed to retrive the most similar chunks of text, it uses cosine similairty to compare the embeddings of the 
# questions with the that of the chunks of paragraphs in vector space.
def similarity(question, embeddings, paragraphs):
    similarity_scores = cosine_similarity([question], embeddings)[0]

    most_similar_indices = np.argsort(similarity_scores)[-3:]

    most_similar_paragraphs = [(paragraphs[i], similarity_scores[i]) for i in most_similar_indices[::-1]]
    most_similar_string = ""
    for paragraph, score in most_similar_paragraphs:
        most_similar_string += paragraph + "\n"
        most_similar_string += "Similarity score: " + str(score) + "\n"

    # Return the top three most similar paragraphs as a string
    return most_similar_string





#This end-point was developed to retrive a response of the question sent by the users.
@app.route('/query', methods=['POST'])
def get_answer():
    data = request.get_json()
    document_id = str(data.get('document_id'))
    question = str(data.get('question'))
    doc_ref = db.collection('users').document(document_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return jsonify({'error': 'Document not found'})

    data = doc.to_dict()
    paragraphs = data.get('Paragraphs') 
    embeddings = data.get('embeddings')

    question_embedding = get_embedding(question)
    embeddings_list = json.loads(embeddings)

    similarity_result = similarity(question_embedding, embeddings_list, paragraphs)
    prompt_result = create_prompt(similarity_result, question)

    generated_answer = generate_answer(prompt_result, 1.0)

    return jsonify({'answer': generated_answer})


 #This end-point was used to return all the documents uploaded by the user.   
@app.route("/dashboard", methods=["POST"])
def dashboard_users():
    try:
        email = request.json["email"]

        if not email:
            return jsonify({"error": "Email is required"}), 400

        user_ref = db.collection('email').document(email)
        user_data = user_ref.get()
    
        if not user_data.exists:
            return jsonify({"error": "Student not found"}), 404

        user_info = user_data.to_dict()

        response = {"message": "User data retrieved", "student_info": user_info}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/deleteItem/', methods=['POST'])
def delete_item():
    try:
        # Ensure the request contains JSON data
        if not request.is_json:
            return jsonify({"error": "Invalid JSON data"}), 400

        # Get data from the request
        user_id = request.json.get('email')
        item_index = request.json.get('itemIndex')

        # Check if required data is present
        if not user_id or item_index is None:
            return jsonify({"error": "Missing required data"}), 400

        user_ref = db.collection('email').document(user_id)

        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()

        if 'files' not in user_data or not isinstance(user_data['files'], list):
            return jsonify({"error": "Invalid user data structure"}), 400

        if item_index < 0 or item_index >= len(user_data['files']):
            return jsonify({"error": f"Invalid item index: {item_index}"}), 400
        
        document_ref_delete = user_data['files'][item_index]['document_id']

        user_data['files'].pop(item_index)
        other_collection_ref = db.collection('users').document(document_ref_delete)
        other_collection_ref.delete()
    

        # Update the Firestore document
        user_ref.update({
            'files': user_data['files']
        })

        return jsonify({"message": "File deleted successfully"}), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500
    

@app.route("/create/user", methods=["POST"])
def create_user():
    try:
        email = request.json["email"]
        json = {
            "name": request.json["name"],
            "email" : request.json["email"],
            "files": []
        }
        db.collection('email').document(email).set(json)

        response = {"message": "User created successfully."}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#This end-point was developed to update the docuement posted by the users.
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    try:
        ref = db.collection('email').document(id)

        files_existing_data = ref.get()
        if not files_existing_data.exists:
            return jsonify({"error": "User data not found"}), 404

        files_updated_data = request.json.get("files")  # Assuming the request body contains the updated "files" array

        ref.update({
            "files": files_updated_data
        })

        response = {"message": "Files updated successfully"}
        return jsonify(response), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
