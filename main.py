import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from stream_utils import Streaming

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

streaming = Streaming()

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/start")
def start_stream(
    source: str = Query("0"), fps: int = Query(30),
    blur: int = Query(0), background: str = Query("None")   
):
    return streaming.list_availavle_devices()

@app.get("/devices")
def devices():
    return streaming.list_availavle_devices()

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000) 
