# src/resume_parser.py
import os
import sys

def parse_pdf_resume(file_path):
    """
    Extract text from a PDF resume.
    """
    try:
        import PyPDF2
    except ImportError:
        sys.exit("Please install PyPDF2 using 'pip install PyPDF2'")

    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def parse_docx_resume(file_path):
    """
    Extract text from a DOCX resume.
    """
    try:
        import docx2txt
    except ImportError:
        sys.exit("Please install docx2txt using 'pip install docx2txt'")
        
    return docx2txt.process(file_path)

if __name__ == "__main__":
    # Example usage:
    sample_pdf = os.path.join("data", "sample_resumes", "sample_resume.pdf")
    sample_docx = os.path.join("data", "sample_resumes", "sample_resume.docx")
    
    if os.path.exists(sample_pdf):
        print("PDF Resume Text:\n", parse_pdf_resume(sample_pdf))
    elif os.path.exists(sample_docx):
        print("DOCX Resume Text:\n", parse_docx_resume(sample_docx))
    else:
        print("No sample resume found in data/sample_resumes")
