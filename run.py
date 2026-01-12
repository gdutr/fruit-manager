import subprocess
import multiprocessing

def run_api():
    """Lance l'API FastAPI."""
    subprocess.run([
        "uvicorn",
        "src.api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

def run_streamlit():
    """Lance l'interface Streamlit."""
    subprocess.run([
        "streamlit", "run",
        "src/ui/acceuil.py",
        "--server.port", "8501"
    ])

if __name__ == "__main__":
    # Lancer les deux processus en parallèle
    api_process = multiprocessing.Process(target=run_api)
    streamlit_process = multiprocessing.Process(target=run_streamlit)
    
    api_process.start()
    streamlit_process.start()
    
    try:
        api_process.join()
        streamlit_process.join()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
        api_process.terminate()
        streamlit_process.terminate()
