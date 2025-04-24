#!/usr/bin/env python3
"""
Resume Coach Application Runner
This script provides a convenient way to run the Resume Coach application
with proper configuration and monitoring.
"""

import uvicorn
import logging
import argparse
from pathlib import Path
import sys
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def check_dependency(module_name):
    """Check if a single dependency is installed."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def check_dependencies():
    """Verify all required dependencies are installed."""
    dependencies = {
        'fastapi': 'fastapi',
        'python-docx': 'docx',
        'PyPDF2': 'PyPDF2',
        'sentence_transformers': 'sentence_transformers'
    }
    
    missing_deps = []
    for package, module in dependencies.items():
        if not check_dependency(module):
            missing_deps.append(package)
            logger.error(f"Missing dependency: {package}")
    
    if missing_deps:
        logger.error(f"Missing dependencies: {', '.join(missing_deps)}")
        logger.info("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    
    logger.info("All required dependencies are installed")
    return True

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['uploads', 'logs', 'data']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_name}")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Resume Coach Application Runner')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    args = parser.parse_args()

    logger.info("Starting Resume Coach application")
    
    # Perform pre-flight checks
    if not check_dependencies():
        logger.error("Dependency check failed")
        sys.exit(1)

    # Setup required directories
    setup_directories()
    
    # Configure uvicorn logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Start the application
    logger.info(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(
        "src.api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_config=log_config,
        log_level="info"
    )

if __name__ == "__main__":
    main() 