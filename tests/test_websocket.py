from time import sleep

from fastapi.testclient import TestClient

from main import app

def test_websocket_get_color():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data[0] == "#"
        assert len(data) == 7

def test_websocket_get_algorithm():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("OpticalFlow")
        sleep(3)
        assert app.tracker.algorithm.__class__.__name__ == "OpticalFlow"
