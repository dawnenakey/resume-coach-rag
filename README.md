# Resume Coach RAG

A Streamlit application that uses RAG (Retrieval-Augmented Generation) technology to analyze resumes and provide real-time job market insights. The application matches resume content against current job requirements and provides actionable insights based on real job market data.

## Features

- Resume parsing support for PDF and DOCX formats
- Real-time job market analysis using Adzuna API
- Semantic similarity matching between resume content and job requirements
- Location-based job market insights
- Technical and soft skills analysis
- File size limit of 200MB per upload

## Technology Stack

- Python 3.10
- Streamlit for the web interface
- Sentence Transformers for semantic analysis
- PyPDF2 and docx2txt for document parsing
- Adzuna API for real-time job market data

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

## Deployment

The application can be deployed using either Railway.app or Render.com.

### Deploying on Render.com

1. The repository includes a `render.yaml` configuration file for easy deployment
2. Connect your GitHub repository to Render.com
3. Create a new Web Service pointing to this repository
4. Render will automatically:
   - Use Python 3.10.12
   - Install dependencies from requirements.txt
   - Set up environment variables
   - Start the Streamlit application

### Deploying on Railway.app

1. Connect your GitHub repository to Railway.app
2. Set up environment variables:
   - `ADZUNA_APP_ID`
   - `ADZUNA_API_KEY`
3. The repository includes:
   - `Dockerfile` for containerized deployment
   - `Procfile` for process management
   - `.dockerignore` for optimized builds

## Environment Variables

The following environment variables are required:

- `ADZUNA_APP_ID`: Your Adzuna API application ID
- `ADZUNA_API_KEY`: Your Adzuna API key

## Project Structure

- `app.py`: Main Streamlit application
- `src/resume_parser.py`: Resume parsing functionality
- `src/semantic_baseline.py`: Semantic analysis implementation
- `.streamlit/config.toml`: Streamlit configuration
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `render.yaml`: Render.com configuration

## Security

- API credentials are stored securely as environment variables
- CORS and XSRF protection enabled
- File upload restrictions in place
- Sensitive files excluded via .gitignore and .dockerignore

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
