# src/resume_parser.py

import os

def parse_pdf_resume(file_path):
    """
    Extract text from a PDF resume.
    """
    try:
        import PyPDF2
    except ImportError as e:
        raise ImportError("PyPDF2 is required to parse PDF files. Install it with 'pip install PyPDF2'") from e

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()

def parse_docx_resume(file_path):
    """
    Extract text from a DOCX resume.
    """
    try:
        import docx2txt
    except ImportError as e:
        raise ImportError("docx2txt is required to parse DOCX files. Install it with 'pip install docx2txt'") from e

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    return docx2txt.process(file_path).strip()
