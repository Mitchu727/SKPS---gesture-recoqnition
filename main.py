from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import cv2 as cv
from algorithms.MeanShift import MeanShift
from algorithms.Tracker import Tracker
import asyncio
import uvicorn

app = FastAPI()
html = ""
with open('html/index.html', 'r') as f:
    html = f.read()

@app.get("/")
async def get(request: Request):
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # TODO find hand
        num = 2
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        # loc_str = open("vtest/vtest_loc.txt", "r").readlines()[num - 1]
        # loc = tuple(map(int, loc_str.split(', ')))
        if cap.isOpened():
            tracker = Tracker(cap)
        while cap.isOpened():
            _, frame = cap.read()
            color = tracker.algorithm.algorithm(frame)
            await websocket.send_text(color)
            await asyncio.wait_for(websocket.receive_text(), timeout=4)
    except WebSocketDisconnect:
        await websocket.close()
        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
