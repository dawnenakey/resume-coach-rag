# src/resume_parser.py

import os
import PyPDF2
import docx2txt
from typing import Optional
import io

def parse_pdf_resume(file) -> str:
    """
    Parse text from a PDF resume file.
    
    Args:
        file: File object (can be path string or file object)
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing PDF file: {str(e)}")

def parse_docx_resume(file) -> str:
    """
    Parse text from a DOCX resume file.
    
    Args:
        file: File object (can be path string or file object)
        
    Returns:
        str: Extracted text from the DOCX
    """
    try:
        # Extract text from DOCX
        text = docx2txt.process(file)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing DOCX file: {str(e)}")

def parse_resume(file) -> Optional[str]:
    """
    Parse text from a resume file (PDF or DOCX).
    
    Args:
        file: Streamlit UploadedFile object or file path
        
    Returns:
        Optional[str]: Extracted text from the resume, or None if file type is not supported
    """
    if hasattr(file, 'name'):  # If it's a Streamlit UploadedFile
        file_name = file.name.lower()
    else:  # If it's a file path string
        file_name = str(file).lower()
        
    if file_name.endswith('.pdf'):
        return parse_pdf_resume(file)
    elif file_name.endswith('.docx'):
        return parse_docx_resume(file)
    else:
        return None
