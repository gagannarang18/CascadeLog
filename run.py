import subprocess
import threading

def run_fastapi():
    subprocess.call(["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    subprocess.call(["streamlit", "run", "app.py", "--server.address=0.0.0.0"])

threading.Thread(target=run_fastapi).start()
run_streamlit()
