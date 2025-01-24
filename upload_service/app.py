import asyncio
import logging
import aio_pika
from flask import request, jsonify, Flask
import os
import boto3
from botocore.client import Config
import json
from dotenv import load_dotenv

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

# Initialize S3 client
s3 = boto3.resource(
    's3',
    endpoint_url=S3_CONFIG["endpoint_url"],
    aws_access_key_id=S3_CONFIG["aws_access_key_id"],
    aws_secret_access_key=S3_CONFIG["aws_secret_access_key"],
    config=Config(signature_version='s3v4'),
    region_name=S3_CONFIG["region_name"]
)

async def send_metadata_to_rabbitmq(email, file_url):
    """Send metadata to the RabbitMQ queue."""
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_CONFIG["url"])
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(RABBITMQ_CONFIG["queue_name"], auto_delete=True)

            message = json.dumps({"email": email, "file_url": file_url})

            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue.name,
            )
            logging.info("Metadata sent to RabbitMQ")
    except Exception as e:
        logging.error(f"Failed to send metadata to RabbitMQ: {e}")

def create_bucket_if_not_exists(bucket_name):
    """Check if S3 bucket exists, and create it if not."""
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except Exception:
        s3.create_bucket(Bucket=bucket_name)

def upload_file_to_s3_bucket(bucket_name, field, file):
    """Upload a file to the S3 bucket."""
    document_name = file.filename
    if not document_name:
        raise ValueError("File must have a name")

    temp_file_path = f"/tmp/{document_name}"
    file.save(temp_file_path)

    s3_key = f"{field}/{document_name}"
    s3.Bucket(bucket_name).upload_file(temp_file_path, s3_key)

    os.remove(temp_file_path)

    file_url = f"{S3_CONFIG['endpoint_url']}/{bucket_name}/{s3_key}"
    return file_url

@app.route('/upload/<field>', methods=['POST'])
def upload_file_endpoint(field):
    """Handle file upload to S3 and send metadata to RabbitMQ."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        create_bucket_if_not_exists(S3_CONFIG["bucket_name"])

        file_url = upload_file_to_s3_bucket(S3_CONFIG["bucket_name"], field, file)

        asyncio.run(send_metadata_to_rabbitmq(field, file_url))

        return jsonify({'message': 'File uploaded successfully', 'file_url': file_url}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        logging.error(f"Error occurred while uploading file: {e}")
        return jsonify({'error': 'Error occurred while uploading file'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
