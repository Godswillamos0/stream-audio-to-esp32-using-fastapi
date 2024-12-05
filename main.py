from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

#uvicorn stream_audio:app --host 0.0.0.0 --port 8000

# Path to the audio file you want to stream
AUDIO_FILE_PATH = "Harvard list 01.wav"  # Replace with your file path

def audio_streamer(file_path: str):
    """
    Generator function to read and yield audio file chunks.
    """
    chunk_size = 1024  # Define the chunk size (1 KB)
    try:
        with open(file_path, "rb") as audio_file:
            while chunk := audio_file.read(chunk_size):
                yield chunk
    except FileNotFoundError:
        raise RuntimeError(f"Audio file not found: {file_path}")


@app.get("/stream-audio")
async def stream_audio():
    """
    Endpoint to stream audio to clients (e.g., ESP32).
    """
    if not os.path.exists(AUDIO_FILE_PATH):
        return Response(content="Audio file not found", status_code=404)

    headers = {
        "Content-Type": "audio/wav",
        "Content-Disposition": f"inline; filename={os.path.basename(AUDIO_FILE_PATH)}",
    }
    return StreamingResponse(audio_streamer(AUDIO_FILE_PATH), headers=headers)

