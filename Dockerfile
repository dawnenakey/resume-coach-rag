# Use an official Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run FastAPI app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
