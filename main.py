import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import cv2 as cv
import uvicorn

from tracklib.Tracker import Tracker

app = FastAPI()
app.camera = None
app.tracker = None
app.mount("/resources", StaticFiles(directory="resources"), name="resources")
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
        app.camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        app.camera.set(cv.CAP_PROP_FPS, 10)
        if app.camera.isOpened():
            # create tracker with chosen algorithm
            app.tracker = Tracker(app.camera)
            await websocket.send_text("LookingFor")
        while app.camera.isOpened():
            # read frame and run step of algorithm
            _, frame = app.camera.read()
            gesture = app.tracker.algorithm.run(frame)
            if gesture is None:
                app.tracker.update_init_loc(app.camera)
            data = app.tracker.color.convert_gesture(gesture)
            print(data)
            # send color | "LookingFor"
            await websocket.send_text(data)
            # confirmation that client recived data, if there is no answer program stopped
            data = await asyncio.wait_for(websocket.receive_text(), timeout=5)
            if data == "FindMyGlove":
                app.tracker.update_init_loc(app.camera)
            elif data != "Received":
                app.tracker.change_algorithm(data, app.camera)
            cv.waitKey(50)
    except Exception:
        print("Connection closed")
    finally:
        await websocket.close()
        app.camera.release()
        app.camera = None
        cv.destroyAllWindows()

# for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
