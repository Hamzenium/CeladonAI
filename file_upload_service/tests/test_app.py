import pytest
from io import BytesIO
from app import app

def test_upload_file_no_file():
    """Test uploading without a file."""
    client = app.test_client()
    response = client.post('/upload/test_field', data={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "No file uploaded"

def test_upload_file_success(mocker):
    """Test successful file upload."""
    client = app.test_client()

    # Mock S3 and RabbitMQ interactions
    mocker.patch("app.create_bucket_if_not_exists")
    mocker.patch("app.upload_file_to_s3_bucket", return_value="https://example.com/test_field/test_file.txt")
    mocker.patch("app.send_metadata_to_rabbitmq")

    data = {
        "file": (BytesIO(b"dummy content"), "test_file.txt")
    }
    response = client.post('/upload/test_field', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.get_json()["message"] == "File uploaded successfully"
    assert "file_url" in response.get_json()

def test_upload_file_invalid_file_name(mocker):
    """Test upload with a file missing a name."""
    client = app.test_client()

    # Mock S3 interactions
    mocker.patch("app.create_bucket_if_not_exists")
    mocker.patch("app.upload_file_to_s3_bucket", side_effect=ValueError("File must have a name"))

    data = {
        "file": (BytesIO(b"dummy content"), "")  # File without a name
    }
    response = client.post('/upload/test_field', data=data, content_type='multipart/form-data')

    assert response.status_code == 400
    assert response.get_json()["error"] == "File must have a name"

def test_upload_file_s3_failure(mocker):
    """Test failure during S3 upload."""
    client = app.test_client()

    # Mock S3 interactions to raise an exception
    mocker.patch("app.create_bucket_if_not_exists")
    mocker.patch("app.upload_file_to_s3_bucket", side_effect=Exception("S3 error"))

    data = {
        "file": (BytesIO(b"dummy content"), "test_file.txt")
    }
    response = client.post('/upload/test_field', data=data, content_type='multipart/form-data')

    assert response.status_code == 500
    assert "error" in response.get_json()
    assert "Error occurred while uploading file" in response.get_json()["error"]
