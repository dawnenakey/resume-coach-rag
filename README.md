# Resume Coach RAG

This project is a RAG-powered job recommender and resume coach that leverages NLP to help job seekers optimize their resumes and find better job matches.

## Local Setup Instructions

1. Clone the repo:
git clone https://github.com/dawnenakey/resume-coach-rag.git
cd resume-coach-rag

2. Create virtual environment and activate:
python3 -m venv venv
source venv/bin/activate # for windows: venv/Scripts/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the app:
uvicorn src.api:app --reload

## Features
- Upload `.pdf` or `.docx` resumes via a FastAPI endpoint
- Extracts and returns plain text from resumes
- FastAPI Swagger UI available at `http://127.0.0.1:8000/docs`
- Modular structure for future extensions (semantic search, RAG models)

## Testing
Use the `/upload_resume/` endpoint via Swagger UI to test file uploads.
Example: Upload `sample_resume.pdf` under `data/sample_resumes/`.

## Project Structure
.
├── data/                     # Sample resumes (optional)
├── src/
│   ├── api.py               # FastAPI app entry point
│   ├── resume_parser.py     # Resume parsing logic
├── uploads/                 # Uploaded resumes (created at runtime)
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md

## Docker (Optional)
1. Build the container:
docker build -t resume-coach .

2. Run the container:
docker run -p 8000:8000 resume-coach

Then open: http://127.0.0.1:8000/docs

## Author
Dawnena Key - [@dawnenakey](https://github.com/dawnenakey)
