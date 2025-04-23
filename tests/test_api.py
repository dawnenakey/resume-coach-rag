import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os

from src.api import app

client = TestClient(app)

@pytest.fixture
def sample_pdf():
    # Create a dummy PDF file for testing
    pdf_content = b"%PDF-1.4\n%EOF"
    pdf_path = Path("tests/fixtures/sample.pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.write_bytes(pdf_content)
    yield pdf_path
    pdf_path.unlink()

def test_read_main():
    """Test that the main page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.text.lower()

def test_upload_invalid_file():
    """Test that uploading an invalid file type returns an error."""
    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = client.post("/upload_resume/", files=files)
    assert response.status_code == 400
    assert "only" in response.json()["detail"].lower()

def test_upload_empty_file():
    """Test that uploading an empty file returns an error."""
    files = {"file": ("test.pdf", b"", "application/pdf")}
    response = client.post("/upload_resume/", files=files)
    assert response.status_code == 422

def test_upload_valid_pdf(sample_pdf):
    """Test that uploading a valid PDF file works."""
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        response = client.post("/upload_resume/", files=files)
    assert response.status_code == 200
    assert "resume_text" in response.text.lower() 