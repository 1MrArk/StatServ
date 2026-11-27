import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Server')))
from app import app, hello_world, token_check, auth, client, admin
from script import token_get

password = os.getenv('PASSWORD')

def test_hello_world():
    response = hello_world()
    assert response == 'Hello World!'

def test_auth():
    with app.test_request_context('/auth?host=test_host&role=script'):
        response = auth()
        assert response.status_code == 200
    with app.test_request_context('/auth?host=test_host&role=admin&password=wrong_password'):
        response = auth()
        assert response.status_code == 401
    with app.test_request_context(f'/auth?host=test_host&role=admin&password={password}'):
        response = auth()
        assert response.status_code == 200
    with app.test_request_context('/auth?host=test_host&role=unknown'):
        response = auth()
        assert response.status_code == 401

"""TODO: Implement token_check tests"""
"""
def test_token_check():
    with app.test_request_context('/auth?host=test_host&role=script'):
        response = auth()
        token = response.get_json()
    @token_check
    def dummy_function():
        return 200
    with app.test_request_context('/client'):
        response = dummy_function()
        assert response.status_code == 401
    with app.test_request_context(f'/client?token={token.text}'):
        assert dummy_function() == 200
"""