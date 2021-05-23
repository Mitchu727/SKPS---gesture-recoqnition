from time import sleep

from fastapi.testclient import TestClient
import cv2 as cv
import pytest

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

# @pytest.mark.parametrize("path", ["vtest/vtest_2.mp4"])
# def test_websocket_change_location(path: str):
#     client = TestClient(app)
#     with client.websocket_connect("/ws") as websocket:
#         prev_loc = app.tracker.init_loc
#         app.camera = cv.VideoCapture(path)
#         websocket.send_text("FindMyGlove")
#         assert prev_loc != app.tracker.init_loc
# TODO nagrać wideo ze znikającą rękawiczką
