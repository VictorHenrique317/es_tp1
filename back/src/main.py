from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from src.database import get_db, MeetingAnalysis
from sqlalchemy.orm import Session
import os
import shutil
from pathlib import Path

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
async def new_video(file : UploadFile = File(...), db: Session = Depends(get_db)):
    last_instance_id  = (
        db.query(MeetingAnalysis)
        .order_by(MeetingAnalysis.id.desc())
        .first()
        .id
    )
    new_id = last_instance_id+1 if last_instance_id else 0
    save_dir = os.path.join(UPLOAD_DIRECTORY,str(new_id))
    video_path = os.path.join(save_dir,file.filename)
    
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
    last_instance_id  = (
        db.query(MeetingAnalysis)
        .order_by(MeetingAnalysis.id.desc())
        .first()
        .id
    )
    new_id = last_instance_id+1 if last_instance_id else 0
    save_dir = os.path.join(UPLOAD_DIRECTORY,str(new_id))
    audio_path = os.path.join(save_dir,file.filename)
    
    db.add(
        MeetingAnalysis(
            media_path= audio_path,
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
    
@app.get("/summary")
async def compute_summary(query_id: int, db: Session = Depends(get_db)):
    meeting_instance  = (
        db.query(MeetingAnalysis)
        .filter_by(id=query_id)
        .first()
    )
    
    if(not meeting_instance.summary_path):
        save_dir = os.path.join(UPLOAD_DIRECTORY,str(meeting_instance.id))
        os.mkdir(save_dir)
        summary_path = os.path.join(save_dir,"summary.txt")
        ## BACKEND CALL HERE
        ##Compute summary and save it at summary_path
        meeting_instance.summary_path = summary_path
        db.commit()
        
    return JSONResponse(status_code=200,
                        content={
                            "link": f"/download/summary/{meeting_instance.id}"
                            }
                        )

@app.get("/download/summary/{instance_id}")
async def download_summary(instance_id: int):
    file_path = os.path.join(UPLOAD_DIRECTORY,str(instance_id),"summary.txt")
    if file_path.exists():
        return FileResponse(path=file_path, filename=f"summary{instance_id}.txt")
    
    raise HTTPException(
        status_code=404,
        detail="The summary of media with id {instance_id} was not computed yet"        
    )


@app.get("/transcription")
async def compute_transcription(query_id: int, db: Session = Depends(get_db)):
    meeting_instance  = (
        db.query(MeetingAnalysis)
        .filter_by(id=query_id)
        .first()
    )
    
    if(not meeting_instance.trascription_path):
        save_dir = os.path.join(UPLOAD_DIRECTORY,str(meeting_instance.id))
        os.mkdir(save_dir)
        transcription_path = os.path.join(save_dir,"transcription.txt")
        ## BACKEND CALL HERE
        ##Compute summary and save it at summary_path
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