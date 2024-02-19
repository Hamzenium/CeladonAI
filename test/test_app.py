import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_scrape_document(client):
    file = open("test/test_data/Database_Architecture.pptx", "rb")
    data = {'file': (file, 'test/test_data/Database_Architecture.pptx')}
    
    response = client.post('/upload/user@example.com', data=data, content_type='multipart/form-data')

    assert response.status_code == 200

    assert 'embeddings' in response.json
    assert 'Paragraphs' in response.json
    assert 'name' in response.json
    assert 'id' in response.json
    assert 'pptx_url' in response.json

    print("Test 'test_scrape_document' passed successfully!")

def test_get_answer(client):
    data = {'document_id': '1bbe5f6f-4bd2-4ac1-860a-a1e05af0f663', 'question': 'What is PwC'}
    
    response = client.post('/query', json=data)


    assert response.status_code == 200

    assert 'answer' in response.json

    print("Test 'test_get_answer' passed successfully!")

def test_dashboard_users(client):

    data = {'email': 'hamza.sohail29@gmail.com'}

    response = client.post('/dashboard', json=data)

    assert response.status_code == 200

    assert 'message' in response.json
    assert 'student_info' in response.json

    print("Test 'test_dashboard_users' passed successfully!")

if __name__ == "__main__":
    pytest.main()