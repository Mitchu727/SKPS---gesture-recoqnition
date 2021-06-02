import asyncio
import sys

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import cv2 as cv
import uvicorn
import time

from tracklib.Tracker import Tracker


app = FastAPI()
# after connecting with websocket set camera to VideoCapture object
app.camera = None
# and set tracker object to manage algorithms
app.tracker = None
app.debug = False

# mount css file
app.mount("/resources", StaticFiles(directory="resources"), name="resources")
# and read html file
html = ""
with open('html/index.html', 'r') as f:
    html = f.read()


@app.get("/")
async def get():
    return HTMLResponse(html)

# websocket endpoint with camera operations
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        if app.camera is None:
            app.camera = cv.VideoCapture(0)
            if app.camera.isOpened():
                # create tracker with chosen algorithm
                app.tracker = Tracker(app.camera)
                await websocket.send_text("LookingFor")
        while app.camera.isOpened():
            # read frame and run step of algorithm
            start = time.time()
            _, frame = app.camera.read()
            gesture = app.tracker.algorithm.run(frame)
            # if the glove is lost
            if gesture is None:
                app.tracker.update_init_loc(app.camera)
            color = app.tracker.color.convert_gesture(gesture)
            # send color | "LookingFor"
            await websocket.send_text(color)
            # confirmation that client recived data, if there is no answer program stopped
            data = await asyncio.wait_for(websocket.receive_text(), timeout=5)
            if data == "FindMyGlove":
                app.tracker.update_init_loc(app.camera)
            elif data != "Received":
                app.tracker.change_algorithm(data, app.camera)
            if app.debug:
                app.tracker.algorithm.draw(frame)
                cv.waitKey(50)
    except Exception:
        print("Connection closed")
    finally:
        # close the websocket and the camera
        await websocket.close()
        if app.camera is None:
            app.camera.release()
            app.camera = None
        if app.debug:
            cv.destroyAllWindows()


if __name__ == "__main__":
    # for debugging and showing camera view
    # change ip in index.html
    if "-d" in sys.argv[1:]:
        app.debug = True
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
