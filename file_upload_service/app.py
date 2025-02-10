import asyncio
import logging
import aio_pika
from flask import request, jsonify, Flask
import os
import boto3
from botocore.client import Config
import json
import hashlib
import time
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

# Flask App
app = Flask(__name__)

# Configuration
S3_CONFIG = {
    "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "region_name": os.getenv("AWS_REGION_NAME"),
    "bucket_name": os.getenv("S3_BUCKET_NAME"),
}

RABBITMQ_CONFIG = {
    "url": os.getenv("RABBITMQ_URL"),
    "queue_name": os.getenv("RABBITMQ_QUEUE_NAME")
}

# Firebase Admin initialization
FIREBASE_KEY_FILE = 'key.json'  # Replace with the actual path to your key.json file
cred = credentials.Certificate(FIREBASE_KEY_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize S3 client
s3 = boto3.resource(
    's3',
    endpoint_url=S3_CONFIG["endpoint_url"],
    aws_access_key_id=S3_CONFIG["aws_access_key_id"],
    aws_secret_access_key=S3_CONFIG["aws_secret_access_key"],
    config=Config(signature_version='s3v4'),
    region_name=S3_CONFIG["region_name"]
)

def create_bucket_if_not_exists(bucket_name):
    """Check if S3 bucket exists, and create it if not."""
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except Exception:
        s3.create_bucket(Bucket=bucket_name)

def upload_file_to_s3_bucket(bucket_name, file):
    """Upload a file to the S3 bucket with a unique name and generate a presigned URL."""
    original_name = file.filename
    if not original_name:
        raise ValueError("File must have a name")
    
    # Generate a unique name using current time and the original filename
    timestamp = str(time.time()).encode()
    unique_name = hashlib.sha256(timestamp + original_name.encode()).hexdigest()
    unique_document_name = f"{unique_name}_{original_name}"

    temp_file_path = f"/tmp/{unique_document_name}"
    file.save(temp_file_path)

    s3_key = f"{unique_document_name}"
    s3.Bucket(bucket_name).upload_file(temp_file_path, s3_key)

    os.remove(temp_file_path)

    # Generate a presigned URL for file access
    presigned_url = s3.meta.client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=3600  # URL expires in 1 hour
    )
    return presigned_url, s3_key

async def send_metadata_to_rabbitmq(email, file_url, s3_key, document_id):
    """Send metadata to the RabbitMQ queue, including the S3 key."""
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_CONFIG["url"])
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=10)

            # Declare the queue to ensure it exists
            await channel.declare_queue(
                RABBITMQ_CONFIG["queue_name"],
                durable=True
            )

            message = json.dumps({
                "email": email,
                "file_url": file_url,
                "s3_key": s3_key,
                "document_id": document_id
            })

            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=RABBITMQ_CONFIG["queue_name"],
            )
            logging.info("Metadata sent to RabbitMQ")
    except Exception as e:
        logging.error(f"Failed to send metadata to RabbitMQ: {e}")

def save_to_firebase( email, document_id, document_name, link):
    """Save metadata to Firebase Firestore."""
    dict = {}
    db.collection('users').document(document_id).set(dict)
    user_ref = db.collection('email').document(email)
    user_data = user_ref.get()

    if not user_data.exists:
        raise ValueError("User not found")

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

@app.route('/upload/<field>', methods=['POST'])
def upload_file_endpoint(field):
    """Handle file upload to S3 and send metadata to RabbitMQ."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    email = field # Expecting email in the form data

    try:
        create_bucket_if_not_exists(S3_CONFIG["bucket_name"])

        file_url, s3_key = upload_file_to_s3_bucket(S3_CONFIG["bucket_name"], file)
        document_id = hashlib.sha256(f"{email}_{time.time()}".encode()).hexdigest()

        asyncio.run(send_metadata_to_rabbitmq(email, file_url, s3_key, document_id))
        document_name = file.filename
        save_to_firebase(email, document_id, document_name, file_url)

        return jsonify({'message': 'File uploaded successfully', 'file_url': file_url, 's3_key': s3_key}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        logging.error(f"Error occurred while uploading file: {e}")
        return jsonify({'error': 'Error occurred while uploading file'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
