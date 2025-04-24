# src/resume_parser.py

import os
import PyPDF2
import docx2txt
from typing import Optional

def parse_pdf_resume(file_path: str) -> str:
    """
    Parse text from a PDF resume file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        with open(file_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing PDF file: {str(e)}")

def parse_docx_resume(file_path: str) -> str:
    """
    Parse text from a DOCX resume file.
    
    Args:
        file_path (str): Path to the DOCX file
        
    Returns:
        str: Extracted text from the DOCX
    """
    try:
        # Extract text from DOCX
        text = docx2txt.process(file_path)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing DOCX file: {str(e)}")

def parse_resume(file_path: str) -> Optional[str]:
    """
    Parse text from a resume file (PDF or DOCX).
    
    Args:
        file_path (str): Path to the resume file
        
    Returns:
        Optional[str]: Extracted text from the resume, or None if file type is not supported
    """
    if file_path.lower().endswith('.pdf'):
        return parse_pdf_resume(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx_resume(file_path)
    else:
        return None
