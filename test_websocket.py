from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data[0] == "#"
        assert len(data) == 7
