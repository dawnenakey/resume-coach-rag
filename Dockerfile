FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8501

# Expose the port
EXPOSE 8501

# Command to run the application
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
