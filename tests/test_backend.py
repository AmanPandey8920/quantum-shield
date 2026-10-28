from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_register_device() -> None:
    response = client.post('/devices/register', json={'device_id': 'ESP32-TEST', 'name': 'Test Device'})
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data


def test_sensor_ingest() -> None:
    response = client.post('/sensor-data', json={'device_id': 'ESP32-TEST', 'temperature': 25.0, 'humidity': 50.0})
    assert response.status_code == 200


def test_ai_analyze() -> None:
    response = client.post('/ai/analyze', json={'temperature': 35.0, 'humidity': 80.0, 'requests_per_minute': 30})
    assert response.status_code == 200
    body = response.json()
    assert 'is_anomaly' in body
