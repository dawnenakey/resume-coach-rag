# Resume Coach RAG

A Streamlit application that uses RAG (Retrieval-Augmented Generation) technology to analyze resumes and provide real-time job market insights. This capstone project combines natural language processing, real-time job market data, and interactive visualizations to help job seekers optimize their resumes.

## Problem Statement

Modern job seekers face several challenges:
- Difficulty in effectively tailoring resumes to specific roles
- Time-consuming manual optimization process
- Risk of missing key skills required by employers
- Misalignment with real-time hiring trends
- Potential elimination by Automated Tracking Systems (ATS)

## Solution

Resume Coach RAG addresses these challenges through:
- Automated resume analysis and skill extraction
- Real-time job market data integration
- Language style analysis for better communication
- Geographic market demand insights
- Salary trends and company hiring patterns

## Features

### Resume Analysis
- Support for PDF and DOCX formats
- Automatic skill categorization (Technical vs Soft Skills)
- Language style analysis (Collaborative/Assertive/Neutral)
- Interactive text analysis visualization

### Market Intelligence
- Real-time job market analysis using Adzuna API
- Location-based insights for major tech hubs
- Trending skills identification
- Top hiring companies by location
- Detailed salary insights by skill

### Visualization & Insights
- Interactive charts using Plotly
- Skill distribution analysis
- Geographic job market trends
- Company hiring patterns
- Salary range comparisons

## Technology Stack

### Core Technologies
- Python 3.10
- Streamlit for web interface
- Sentence Transformers for semantic analysis
- spaCy for natural language processing
- PyPDF2 and docx2txt for document parsing

### APIs and Data Sources
- Adzuna API for real-time job market data
- Custom keyword extraction system
- Semantic similarity matching

### Deployment Options
- Docker containerization
- Streamlit Cloud deployment - current application is successful at https://dawnenaresumecoach.streamlit.app/
- Railway.app alternative deployment
- Render.com configuration

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/dawnenakey/resume-coach-rag.git
cd resume-coach-rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file with your Adzuna API credentials:
```toml
ADZUNA_APP_ID = "your_app_id"
ADZUNA_API_KEY = "your_api_key"
```

4. Run the application:
```bash
streamlit run app.py
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t resume-coach .
```

2. Run the container:
```bash
docker run -p 8501:8501 -e ADZUNA_APP_ID=your_app_id -e ADZUNA_API_KEY=your_api_key resume-coach
```

## Project Structure

```
resume-coach-rag/
├── app.py                 # Main Streamlit application
├── src/
│   ├── resume_parser.py   # Resume parsing functionality
│   ├── semantic_baseline.py # Semantic analysis implementation
│   └── adzuna_api.py      # Job market data integration
├── .streamlit/
│   ├── config.toml        # Streamlit configuration
│   └── secrets.toml       # API credentials (git-ignored)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Container orchestration
└── render.yaml          # Render.com configuration
```

## Key Components

### Resume Parser
- Supports multiple document formats
- Extracts text while preserving structure
- Handles various resume layouts

### Semantic Analysis
- Language style assessment
- Skill categorization
- Keyword extraction and matching

### Market Analysis
- Real-time job market data
- Salary range analysis
- Company hiring trends
- Geographic demand patterns

## Security Considerations

- API credentials stored as environment variables
- Secure file upload handling
- Rate limiting implemented
- CORS and XSRF protection
- Sensitive file exclusion via .gitignore

## Future Enhancements

- Enhanced ATS compatibility scoring
- Industry-specific resume recommendations
- Interview question generation
- Career path suggestions
- Expanded geographic coverage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Adzuna API for job market data
- Streamlit for the web framework
- Sentence Transformers for semantic analysis
- The open-source community for various tools and libraries
