import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import threading

from stream_utils import Streaming
from fastapi import Query

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

streaming = Streaming()

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/start")
def start_stream(
    source: str = Query("0"), fps: int = Query(15),
    blur_strength: int = Query(21), background: str = Query("None")
):
    streaming.update_streaming_config(
        in_source=source, out_source=None, fps=fps, blur_strength=blur_strength, background=background
    )

    if streaming.running:
        return JSONResponse(content={"message": "Streaming is already running."}, status_code=400)
    
    stream_thread = threading.Thread(target=streaming.stream_video, args=())
    stream_thread.start()

    return {"message": f"Streaming started from source {source} at {fps} FPS and blur strength : {blur_strength}."}

@app.get("/devices")
def devices():
    return streaming.list_available_devices()

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000) 
