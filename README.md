# Resume Coach RAG

A Streamlit-powered application that analyzes resumes using RAG (Retrieval-Augmented Generation) technology to provide insights and improvement suggestions.

## Features

- Resume analysis (PDF and DOCX support)
- Technology stack analysis
- Gender bias detection
- Skills coverage visualization
- Real-time feedback and suggestions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Upload your resume (PDF or DOCX format)
2. Wait for the analysis to complete
3. Review the insights and suggestions
4. Use the feedback to improve your resume

## Technologies Used

- Streamlit for the web interface
- Plotly for data visualization
- Sentence Transformers for text analysis
- PyPDF2 and python-docx for document parsing

## Project Overview
An intelligent system that analyzes resumes using NLP and machine learning to:
- Detect and reduce bias in resume screening
- Provide quantitative matching against job descriptions
- Generate actionable feedback for job seekers

## Live Demo Results
Here's a sample analysis of actual results:

### Keyword Analysis
```
Cloud Technologies: ██████████████ (12 mentions)
API Development:    █████████ (9 mentions)
Azure Platform:     ████████ (8 mentions)
Python:            █ (1 mention)
Leadership:        █ (1 mention)
AWS:              ░ (0 mentions)
```

### Bias Detection
```
Femininity Score:  0.0901 [▓░░░░░░░░░] 9.01%
Masculinity Score: 0.1175 [▓░░░░░░░░░] 11.75%
Balance Score:     0.9725 [█████████▓] 97.25%
```

### Performance Metrics
- Processing Time: 2.68s
- Success Rate: 92%
- GPU Acceleration: MPS (Metal Performance Shaders)

## Key Features
- PDF and DOCX resume parsing
- Gender bias detection
- Keyword frequency analysis
- Job description similarity scoring
- Real-time analysis with GPU acceleration

## Technical Architecture
- **Backend**: FastAPI
- **ML Models**: Sentence Transformers
- **Processing**: PyPDF2, python-docx
- **Testing**: pytest
- **CI/CD**: GitHub Actions
- **Acceleration**: Metal Performance Shaders (MPS)

## Installation

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)
- Mac with Apple Silicon (for MPS acceleration) or CPU-only mode

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-analysis-system.git
cd resume-analysis-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the server:
```bash
./run.py --reload
```

2. Access the web interface:
- Open http://127.0.0.1:8000 in your browser
- Upload a resume (PDF/DOCX)
- View analysis results

## Development

### Project Structure
```
resume-analysis-system/
├── src/                    # Source code
│   ├── api.py             # FastAPI application
│   ├── resume_parser.py   # Resume parsing logic
│   └── semantic_baseline.py# Analysis models
├── tests/                  # Test suite
├── docs/                   # Documentation
├── uploads/               # Temporary file storage
├── requirements.txt       # Dependencies
├── run.py                # Application runner
└── Dockerfile            # Container definition
```

### Running Tests
```bash
pytest
```

### Code Style
- Black for formatting
- isort for import sorting
- flake8 for linting

## API Documentation

### Endpoints

#### POST /upload_resume/
Upload and analyze a resume:
```python
response = await client.post(
    "/upload_resume/",
    files={"file": ("resume.pdf", file_content)}
)
```

Response:
```json
{
    "resume_text": "...",
    "scores": {
        "femininity_score": 0.0901,
        "masculinity_score": 0.1175
    },
    "keyword_freq": {
        "python": 1,
        "cloud": 12,
        "api": 9
    },
    "similarity_score": 0.50
}
```

## Performance

### Processing Speed
- Average analysis time: 2.68s per resume
- GPU-accelerated inference using MPS
- 92% successful analysis rate

### Resource Usage
- Memory: ~500MB baseline
- GPU: Optimized for Apple Silicon
- Storage: Temporary file cleanup

## Future Improvements
1. Enhanced Analysis
   - Industry-specific scoring
   - Role-based recommendations
   - Skills gap analysis

2. Technical Improvements
   - Support for more file formats
   - Improved PDF parsing
   - Real-time analysis
   - API rate limiting

3. ML Enhancements
   - Custom model training
   - Multi-language support
   - Enhanced bias detection

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Author
**Dawnena Key**
- Email: dawnena.key@du.edu
- GitHub: [@dawnenakey](https://github.com/dawnenakey/resume-coach-rag)

## Acknowledgments
- Sentence Transformers team
- FastAPI community
- PyPDF2 maintainers
