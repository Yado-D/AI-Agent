from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from agent import generate_response
from wisper import audio_to_text
from gtt import text_to_audio

app = FastAPI(title="AI Voice/Text Agent API")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Voice/Text Agent API is running!"}

class TextRequest(BaseModel):
    prompt: str

@app.post("/chat/text")
async def chat_text(request: TextRequest):
    try:
        response_text = generate_response(request.prompt)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/voice")
async def chat_voice(file: UploadFile = File(...)):
    input_path = "temp_input.mp3"
    output_path = "temp_output.mp3"
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Transcribe audio to text
        transcribed_text = audio_to_text(input_path)
        
        # Get AI Response
        ai_response = generate_response(transcribed_text)
        
        # Convert response to audio
        text_to_audio(ai_response, output_path)
        
        return FileResponse(
            output_path, 
            media_type="audio/mpeg",
            filename="response.mp3" # Name of downloaded file 
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

if __name__ == "__main__":
    import uvicorn
    # Make sure to bind to 0.0.0.0 and the PORT provided by Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
