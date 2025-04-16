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
