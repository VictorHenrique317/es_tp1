from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.database import get_db, MeetingAnalysis
from sqlalchemy.orm import Session
import os
import json
import asyncio
import shutil
from pathlib import Path
from faster_whisper import WhisperModel


UPLOAD_DIRECTORY = "/home/victor/Projects/es_tp1/back/uploads/"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_NAME = "summarizer"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: Create upload directory
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    
    # Yield control to the application
    yield
    
    # Shutdown event: (You can add any cleanup code here if needed)
    print("Server is shutting down...")



app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/video")
async def new_video(file : UploadFile = File(...), db: Session = Depends(get_db)):
    new_id = db.query(MeetingAnalysis).count() + 1
    save_dir = os.path.join(UPLOAD_DIRECTORY,str(new_id))
    os.makedirs(save_dir, exist_ok=True)
    video_path = os.path.join(save_dir,file.filename)
    print(new_id)
    db.add(
        MeetingAnalysis(
            media_path= video_path,
        )
    )
    db.commit()
    
    with open(video_path, "wb") as buffer: # salva o video no disco
        shutil.copyfileobj(file.file,buffer)
        
    # TODO: tratar excessoes
    return JSONResponse(status_code=201,
                        content={
                            "message": "audio processed sucessfully",
                            "db_id":new_id
                            }
                        )

@app.post("/audio")
async def new_audio(file : UploadFile = File(...), db: Session = Depends(get_db)):
    new_id = db.query(MeetingAnalysis).count() + 1
    print(new_id)
    save_dir = os.path.join(UPLOAD_DIRECTORY,str(new_id))
    os.makedirs(save_dir, exist_ok=True)
    audio_path = os.path.join(save_dir,file.filename)
    
    db.add(
        MeetingAnalysis(
            media_path= audio_path
        )
    )
    db.commit()
    
    with open(audio_path, "wb") as buffer: # salva o video no disco
        shutil.copyfileobj(file.file,buffer)
        
    # TODO: tratar excessoes
    return JSONResponse(status_code=201,
                        content={
                            "message": "audio processed sucessfully",
                            "db_id":new_id
                            }
                        )
    
async def run_curl_async(text: str):
    # Run the curl command asynchronously
    data = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": text,
        "stream": False
    }
    payload = json.dumps(data)
    process = await asyncio.create_subprocess_exec(
        'curl', OLLAMA_URL, '-d', payload,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()  # Wait for the process to finish
    print(type(stdout))
    print(stdout)
    print("saiu")
    if process.returncode == 0:
        return json.loads(stdout.decode())
    else:
        error_msg = stderr.decode()
        raise Exception(f"Curl command failed with error: {error_msg}")

async def summarize(transcription_path: str):
    with open(transcription_path, 'r') as f:
        full_text = f.read()
    
    print(full_text)
    
    try:
        curl_response = await run_curl_async(full_text)
        print(curl_response)
        print("cima")
        return curl_response["response"] # return the full summary
    except Exception as e:
        # Handle the generic exception
        print("aqui")
        raise Exception(str(e))


@app.get("/summary")
async def compute_summary(query_id: int, db: Session = Depends(get_db)):
    meeting_instance  = (
        db.query(MeetingAnalysis)
        .filter_by(id=query_id)
        .first()
    )
    
    if(not meeting_instance.summary_path):
        save_dir = os.path.join(UPLOAD_DIRECTORY,str(meeting_instance.id))
        summary_path = os.path.join(save_dir,"summary.txt")
        transcription_path = os.path.join(save_dir, "transcription.txt")
        try:
            if (not meeting_instance.transcription_path):
                transcription = transcribe(meeting_instance.media_path, transcription_path)
                with open(transcription_path,'w') as f:
                    f.write(transcription)
            summary = await summarize(transcription_path)
            with open(summary_path, 'w') as f:
                f.write(summary)
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"error during the models processing:\n{str(e)}"        
            )
        meeting_instance.summary_path = summary_path
        db.commit()
        
    return JSONResponse(status_code=200,
                        content={
                            "link": f"/download/summary/{meeting_instance.id}"
                            }
                        )

@app.get("/download/summary/{instance_id}")
async def download_summary(instance_id: int):
    file_path = Path(os.path.join(UPLOAD_DIRECTORY,str(instance_id),"summary.txt"))
    if file_path.exists():
        return FileResponse(path=file_path, filename=f"summary{instance_id}.txt")
    
    raise HTTPException(
        status_code=404,
        detail="The summary of media with id {instance_id} was not computed yet"        
    )


def transcribe(media_path, transcription_path):
    transcription = ""
    transcription_model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    segments, info = transcription_model.transcribe(media_path, beam_size=5)
    del transcription_model
    for segment in segments:
        transcription += segment.text + "\n"
    return transcription

@app.get("/transcription")
async def compute_transcription(query_id: int, db: Session = Depends(get_db)):
    meeting_instance  = (
        db.query(MeetingAnalysis)
        .filter_by(id=query_id)
        .first()
    )
    
    if(not meeting_instance):
        raise HTTPException(
        status_code=404,
        detail=f"The media with id {query_id} was not found"        
    )
    
    if(not meeting_instance.trascription_path):
        print("entrei")
        save_dir = os.path.join(UPLOAD_DIRECTORY,str(meeting_instance.id))
        transcription_path = os.path.join(save_dir,"transcription.txt")
        transcription = transcribe(meeting_instance.media_path, transcription_path)
        with open(transcription_path,'w') as f:
            f.write(transcription)
        meeting_instance.trascription_path = transcription_path
        db.commit()
        
    return JSONResponse(status_code=200,
                        content={
                            "link": f"/download/transcription/{meeting_instance.id}"
                            }
                        )
    
@app.get("/download/transcription/{instance_id}")
async def download_transcription(instance_id: int):
    file_path = Path(os.path.join(UPLOAD_DIRECTORY,str(instance_id),"transcription.txt"))
    if file_path.exists():
        return FileResponse(path=file_path, filename=f"transcription{instance_id}.txt")
    
    raise HTTPException(
        status_code=404,
        detail=f"The transcription of media with id {instance_id} was not computed yet"        
    )
