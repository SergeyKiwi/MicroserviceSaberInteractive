from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_build_ok():
    build = 'front_arm'
    response = client.post("/POST/get_tasks", json={"build": build})
    assert response.status_code == 200
    assert type(response.json()['tasks']) == list


def test_get_build_empty():
    build = ''
    response = client.post("/POST/get_tasks", json={'build': build})
    assert response.status_code == 404
    assert response.json() == {'Error': 'Build not found'}


def test_error_json():
    build = 'forward_interest'
    response = client.post("/POST/get_tasks", json={'test': build})
    assert response.status_code == 400
    assert response.json() == {'Error': 'Invalid JSON request!'}
