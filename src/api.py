# src/api.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, Optional
import shutil
import os
import logging
from pathlib import Path

from src.resume_parser import parse_pdf_resume, parse_docx_resume
from src.semantic_baseline import baseline_scores, extract_keywords
from src.scoring import compute_similarity_score

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom exceptions
class ResumeParsingError(Exception):
    """Raised when there's an error parsing the resume file."""
    pass

class FileStorageError(Exception):
    """Raised when there's an error storing or accessing the uploaded file."""
    pass

app = FastAPI(
    title="Resume Coach RAG",
    description="A RAG-powered job recommender and resume coach",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.get("/")
async def form_page(request: Request) -> templates.TemplateResponse:
    """
    Render the main form page for resume upload.

    Args:
        request: The incoming request object

    Returns:
        TemplateResponse: The rendered form template
    """
    return templates.TemplateResponse("form.html", {"request": request})

def validate_file(file: UploadFile) -> None:
    """
    Validate the uploaded file meets requirements.

    Args:
        file: The uploaded file to validate

    Raises:
        HTTPException: If file validation fails
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are supported"
        )

@app.post("/upload_resume/", response_class=JSONResponse)
async def upload_resume(
    request: Request,
    file: UploadFile = File(...)
) -> templates.TemplateResponse:
    """
    Process uploaded resume file and return analysis results.

    Args:
        request: The incoming request object
        file: The uploaded resume file

    Returns:
        TemplateResponse: Analysis results rendered in template

    Raises:
        HTTPException: For various error conditions during processing
    """
    try:
        # Validate uploaded file
        validate_file(file)
        logger.info(f"Processing file: {file.filename}")

        # Save file
        file_path = UPLOAD_DIR / file.filename
        try:
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
            raise FileStorageError("Failed to save uploaded file")

        # Extract resume text
        try:
            if file_path.suffix.lower() == ".pdf":
                resume_text = parse_pdf_resume(str(file_path))
            else:
                resume_text = parse_docx_resume(str(file_path))
        except Exception as e:
            logger.error(f"Failed to parse resume: {str(e)}")
            raise ResumeParsingError("Failed to parse resume content")

        # Perform analysis
        try:
            scores = baseline_scores(resume_text)
            keyword_freq = extract_keywords(resume_text)
            
            baseline_job_description = """
            We are looking for a detail-oriented software engineer who has experience with Python, 
            API development, and cloud platforms like Azure or AWS.
            """
            similarity_score = compute_similarity_score(resume_text, baseline_job_description)
            
            logger.info(f"Successfully analyzed resume for {file.filename}")
            
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "resume_text": resume_text[:1000],
                    "scores": scores,
                    "keyword_freq": keyword_freq,
                    "similarity_score": similarity_score
                }
            )
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to analyze resume content"
            )

    except FileStorageError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ResumeParsingError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
    finally:
        # Clean up uploaded file
        try:
            if 'file_path' in locals():
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up file: {str(e)}")
