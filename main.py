from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import cv2 as cv
from algorithms.Tracker import Tracker
import asyncio
import uvicorn

app = FastAPI()
html = ""
with open('html/index.html', 'r') as f:
    html = f.read()

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if cap.isOpened():
            # create tracker with chosen algorithm
            tracker = Tracker(cap)
        while cap.isOpened():
            # read frame and run step of algorithm
            _, frame = cap.read()
            color = tracker.algorithm.run(frame)
            print(color)
            # send color
            await websocket.send_text(color)
            # confirmation that client recived data, if there is no answer program stopped
            await asyncio.wait_for(websocket.receive_text(), timeout=5)
    except WebSocketDisconnect:
        await websocket.close()
        cap.release()
        cv.destroyAllWindows()

# for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
