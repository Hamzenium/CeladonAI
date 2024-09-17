from firebase_admin import firestore, storage
import json

db = firestore.client()
bucket = storage.bucket("celadonai-69915.appspot.com")

def save_to_firebase(data, email, document_id, document_name, link):
    user_ref = db.collection('email').document(email)
    user_data = user_ref.get()

    if not user_data.exists:
        raise Exception("User not found")

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
    db.collection('users').document(document_id).set(data)

def get_user_documents(email):
    user_ref = db.collection('email').document(email)
    user_data = user_ref.get()
    if not user_data.exists:
        raise Exception("User not found")
    return user_data.to_dict()

def delete_document(user_id, item_index):
    user_ref = db.collection('email').document(user_id)
    user_data = user_ref.get().to_dict()
    if 'files' not in user_data or not isinstance(user_data['files'], list):
        raise Exception("Invalid user data structure")

    document_id = user_data['files'][item_index]['document_id']
    user_data['files'].pop(item_index)
    user_ref.update({'files': user_data['files']})
    db.collection('users').document(document_id).delete()
