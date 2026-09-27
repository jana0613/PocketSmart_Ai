import os
os.environ['DATABASE_PATH'] = 'data/test_pocketsmart.db'
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['GEMINI_API_KEY'] = ''

from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        r = client.get('/api/health')
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'

def test_register_login_home():
    email = 'test@example.com'
    with TestClient(app) as client:
        client.post('/api/auth/register', json={'email': email, 'password': 'password123'})
        r = client.post('/api/auth/login', json={'email': email, 'password': 'password123'})
        assert r.status_code == 200
        token = r.json()['access_token']
        r = client.post('/api/planners/home', headers={'Authorization': f'Bearer {token}'}, json={'budget': 50000, 'currency': 'INR', 'items': [{'room': 'Living Room', 'item': 'sofa', 'quantity': 1, 'style': 'Modern'}], 'priorities': []})
        assert r.status_code == 200
        assert r.json()['source'] == 'fallback'
        assert r.json()['remaining_budget'] >= 0

def test_jewelry_requires_auth():
    with TestClient(app) as client:
        r = client.post('/api/planners/jewelry', data={'budget': 10000, 'currency': 'INR', 'occasion': 'Party', 'style': 'Elegant', 'metal': 'Any', 'outfit_notes': ''})
        assert r.status_code == 401
