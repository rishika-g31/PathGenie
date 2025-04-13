import pytest
from run import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as client:
        yield client

def test_signup_success(client):
    email = 'testuser9@example.com'
    response = client.post('/auth/signup', data={
        'email': email,
        'password': 'securepass123',
        'confirm_password': 'securepass123'
    }, follow_redirects=True)
    # print(response.data.decode())
    assert response.status_code == 200 
    assert b'Dummy Dashboard for Testing' in response.data
    print(response.data.decode())  # Add in your test

    
def test_login_success(client):
    email = 'testuser9@example.com'

    response = client.post('/auth/login', data={
        'email': email,
        'password': 'securepass123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Dummy Dashboard for Testing' in response.data