from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
import shutil
from models import MeetingAnalysis

UPLOAD_DIRECTORY = "./uploads/"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: Create upload directory
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    
    # Yield control to the application
    yield
    
    # Shutdown event: (You can add any cleanup code here if needed)
    print("Server is shutting down...")



app = FastAPI(lifespan=lifespan)

@app.post("/video")
def process_video(file : UploadFile = File(...), db: Session = Depends(get_db)):
    last_instance_id  = (
        db.query(MeetingAnalysis)
        .order_by(MeetingAnalysis.id.desc())
        .first()
    )
    new_id = last_instance_id+1 if last_instance_id else 0
    save_dir = os.path.join(UPLOAD_DIRECTORY,str(new_id))
    video_path = os.path.join(save_dir,file.filename)
    transcription_path = os.path.join(save_dir,"transcription.txt")
    summary_path = os.path.join(save_dir,"summary.txt")
    
    ### COMPUTAR TRANSCRICAO E RESUMO AQUI
    
    ###
    
    db.add(
        MeetingAnalysis(
            media_path= video_path,
            transcription_path = transcription_path,
            summary_path = summary_path
        )
    )
    
    with open(video_path, "wb") as buffer: # salva o video no disco
        shutil.copyfileobj(file.file,buffer)

    ## SALVAR TRANSCRICAO E RESUMO EM DISCO AQUI
    
    ###    
        
    # TODO: tratar excessoes
    return JSONResponse(status_code=201, content={"message": "Video processed sucessfully"})

@app.post("/audio")
def process_video(file : UploadFile = File(...), db: Session = Depends(get_db)):
    last_instance_id  = (
        db.query(MeetingAnalysis)
        .order_by(MeetingAnalysis.id.desc())
        .first()
    )
    new_id = last_instance_id+1 if last_instance_id else 0
    save_dir = os.path.join(UPLOAD_DIRECTORY,str(new_id))
    audio_path = os.path.join(save_dir,file.filename)
    transcription_path = os.path.join(save_dir,"transcription.txt")
    summary_path = os.path.join(save_dir,"summary.txt")
    
    ### COMPUTAR TRANSCRICAO E RESUMO AQUI
    
    ###
    
    db.add(
        MeetingAnalysis(
            media_path= audio_path,
            transcription_path = transcription_path,
            summary_path = summary_path
        )
    )
    
    with open(audio_path, "wb") as buffer: # salva o video no disco
        shutil.copyfileobj(file.file,buffer)

    ## SALVAR TRANSCRICAO E RESUMO EM DISCO AQUI
    
    ###    
        
    # TODO: tratar excessoes
    return JSONResponse(status_code=201, content={"message": "Video processed sucessfully"})
