# src/api.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import shutil
import os

from src.resume_parser import parse_pdf_resume, parse_docx_resume
from src.semantic_baseline import baseline_scores, extract_keywords
from src.scoring import compute_similarity_score

app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_resume/", response_class=JSONResponse)
async def upload_resume(request: Request, file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Only .pdf and .docx files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract resume text
    if file_ext == ".pdf":
        resume_text = parse_pdf_resume(file_path)
    else:
        resume_text = parse_docx_resume(file_path)

    # Analysis
    scores = baseline_scores(resume_text)
    keyword_freq = extract_keywords(resume_text)

    baseline_job_description = """
    We are looking for a detail-oriented software engineer who has experience with Python, API development, and cloud platforms like Azure or AWS.
    """
    similarity_score = compute_similarity_score(resume_text, baseline_job_description)

    # Render the HTML result
    return templates.TemplateResponse("result.html", {
        "request": request,
        "resume_text": resume_text[:1000],
        "scores": scores,
        "keyword_freq": keyword_freq,
        "similarity_score": similarity_score
    })
