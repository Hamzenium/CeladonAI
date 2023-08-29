from flask import Flask, request, jsonify
from pptx import Presentation
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
import uuid 
import firebase_admin       
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("key.json")
import pinecone      

pinecone.init(      
	api_key='96c245fe-c521-4a67-87eb-ba5faacbe2dc',      
	environment='us-west1-gcp-free'      
)      
index = pinecone.Index('celadonai')
firebase_admin.initialize_app(cred)

db = firestore.client()
user_ref = db.collection('user')



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
            document_name = pptx_file.filename
            os.remove(filepath)
           # Save the extracted data to
            embeddings_json = json.dumps(embeddings)

            data = {
                'embeddings': embeddings_json,  # Convert the embeddings to strings
                'Paragraphs': paragraphs,
                'name': document_name
            }

            # Generate a unique document ID using UUID
            document_id = str(uuid.uuid4())
            ucid = "EUmaAfR4UiUtmH8u7gwyATp0g5s2"

            # Push the data to Firestore
            db.collection('users').document(document_id).set(data)
            return jsonify({'embeddings': embeddings, 'Paragraphs':paragraphs, 'name': document_name , "ucid": ucid})

        except Exception as e:
            return jsonify({'error': 'Error occurred while extracting text: {}'.format(str(e))})

    else:
        return jsonify({'error': 'Invalid file format. Only PowerPoint files are supported.'})
     
def create_prompt(context, query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Please come up with another question'\n"
    final = header + context + "\n\n" + query + "\n"
    return final 



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



@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    document_id = str(data.get('document_id'))
    question = str(data.get('question'))
    doc_ref = db.collection('users').document(document_id)
    doc = doc_ref.get()
    if not doc.exists:
        return jsonify({'error': 'Document not found'})
    
    data = doc.to_dict()
    paragraphs = data.get('paragraphs')
    embeddings = data.get('embeddings')

    question_embedding = get_embedding(question)
    embeddings_list = json.loads(embeddings)
    print("first paragrapgh")


    # Convert embeddings back to the original data structure


    similarity_result = similarity(question_embedding, embeddings_list, paragraphs)
    prompt_result = create_prompt(similarity_result, question)
    generated_answer = generate_answer(prompt_result)


    return jsonify({'answer': generated_answer})


if __name__ == '__main__':
    app.run(debug=True)


