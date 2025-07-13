import subprocess
import threading
import time
import sys

def run_fastapi():
    try:
        print("🔵 Starting FastAPI server on port 8000...")
        subprocess.run(
            [
                "uvicorn",
                "server:app",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            check=True  # Raises error if fails
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ FastAPI server failed to start: {e}")
        sys.exit(1)

def run_streamlit():
    time.sleep(5)  # Wait for FastAPI to be ready
    try:
        print("🟢 Starting Streamlit app on port 8501...")
        subprocess.run(
            [
                "streamlit",
                "run",
                "app.py",
                "--server.address=0.0.0.0",
                "--server.port=8501"
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit app failed to start: {e}")
        sys.exit(1)

def main():
    print("🚀 Launching CascadeLog system...")
    
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    run_streamlit()

    # Optional: block main thread if needed
    fastapi_thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"❗ Unexpected error: {e}")
        sys.exit(1)
