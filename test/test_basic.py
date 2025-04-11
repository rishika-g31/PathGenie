import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert b'PathGenie' in response.data
