from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import assemblyai as aai
import os

app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)
    
aai.settings.api_key = os.getenv("API")
FILE_URL = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

@app.post("/text")
def text(url: str=Form(...)):
    try:
        r=""
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(url)
        if transcript.status == aai.TranscriptStatus.error:
            r=transcript.error
        else:
            r=transcript.text
        
        return {"status":"Success", "det":f"{r}"}
    
    except Exception as e:
        return {"status":"Failed", "det":f"{HTTPException(status_code=500, detail=str(e))}"}



# Testing / Ping...
@app.get("/test")
def hello():
    try:
        return {"Success":"API is live."}
    except Exception as e:
        return {"Failed":str(e)}
