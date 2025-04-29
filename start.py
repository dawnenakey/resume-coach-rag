import os
import subprocess
import sys

def main():
    # Get the port from Railway's environment variable, default to 8501
    port = os.environ.get("PORT", "8501")
    
    # Construct the Streamlit command
    cmd = [
        "streamlit",
        "run",
        "app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.serverAddress", "0.0.0.0",
        "--server.enableCORS", "true",
        "--server.enableXsrfProtection", "true"
    ]
    
    # Run the Streamlit application
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 