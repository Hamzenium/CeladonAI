from flask import Flask, request, jsonify
from pptx import Presentation
import numpy as np
import json
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
import asyncio
import uuid 
import firebase_admin       
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("key.json")
    

firebase_admin.initialize_app(cred)

db = firestore.client()
user_ref = db.collection('user')



app = Flask(__name__)
openai.api_key = "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"


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


#This end-point was developed to scrape the text from the ppt and store in chunks on firebase.
@app.route('/upload/<field>', methods=['POST'])
def scrape_pptx(field):
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    pptx_file = request.files['file']
    ucid = field


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
            document_name = pptx_file.filename
            os.remove(filepath)
           # Save the extracted data to
            document_id = str(uuid.uuid4())
            embeddings_json = json.dumps(embeddings)

            data = {
                'embeddings': embeddings_json,  # Convert the embeddings to strings
                'Paragraphs': paragraphs,
                'name': document_name,
                'ucid': ucid,
                'document_id': document_id
            }

            # Generate a unique document ID using UUID

            # Push the data to Firestore
            db.collection('users').document(document_id).set(data)
            return jsonify({'embeddings': embeddings, 'Paragraphs':paragraphs, 'name': document_name , "ucid": ucid, "id": document_id})

        except Exception as e:
            return jsonify({'error': 'Error occurred while extracting text: {}'.format(str(e))})

    else:
        return jsonify({'error': 'Invalid file format. Only PowerPoint files are supported.'})



def create_prompt(context, query):
    header = '''I want you to act as a document that I am having a conversation with. Your name is "AI Assistant". You will provide me with answers from the given info. If the answer is not included, say exactly "Hmm, I am not sure." and stop after that. Refuse to answer any question not about the info. Never break character.'''
    final = header + context + "\n\n" + query + "\n"
    return final 




#This end-point retrives the answer through the API call from the davinci LLM.
def generate_answer(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].text).strip()




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
async def get_answer():
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

    # Convert embeddings back to the original data structure

    similarity_result = similarity(question_embedding, embeddings_list, paragraphs)
    prompt_result = create_prompt(similarity_result, question)


    loop = asyncio.get_event_loop()
    generated_answer = await loop.run_in_executor(None, lambda: generate_answer(prompt_result))

    return jsonify({'answer': generated_answer})




#This end-point was developed to retrive all the docuements posted by the users.
@app.route('/dashboard/<field>', methods=['GET'])
def dashboard(field):
    try:
        user_search = field
        user_ref = db.collection('users')  
        snapshot = user_ref.get()

        array = []
        for doc in snapshot:
            word = doc.to_dict()['ucid']
            if user_search in word:
                array.append(doc.to_dict())

        return jsonify(array)
    except Exception as error:
        return str(error)
    

    
#This end-point was developed to delete a specific docuement posted by the user.
@app.route('/delete/<field>', methods=['GET', 'DELETE'])
def delete(field):
    try:
        user_search = field
        user_ref = db.collection('users').document(user_search)
        user_ref.delete()
        
        return jsonify({'message': 'Document deleted successfully'})
    except Exception as error:
        return jsonify({'error': str(error)})
    


#This end-point was developed to update the docuement posted by the users.
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    try:
        ref = db.collection('users').document(id)

        existing_data = ref.get()
        if not existing_data.exists:
            return jsonify({"error": "Lab data not found"}), 404

        update_data = request.json  # Assuming the request body contains the updated fields as JSON

        ref.update(update_data)

        return jsonify({"message": "Lab data updated successfully"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)


