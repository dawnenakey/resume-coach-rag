from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from src.resume_parser import parse_pdf_resume, parse_docx_resume

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Only .pdf and .docx files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    if file_ext == ".pdf":
        resume_text = parse_pdf_resume(file_path)
    else:
        resume_text = parse_docx_resume(file_path)

    return JSONResponse(content={"filename": file.filename, "extracted_text": resume_text[:1000]})

