from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse

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
    color = "#7FFFD4"
    while color != "q":
        color = input("Podaj kolor: ")
        await websocket.send_text(color)
    await websocket.close()