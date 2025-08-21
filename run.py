import subprocess
import multiprocessing
import uvicorn

def run_api():
    uvicorn.run("main:app", port=8000, log_level="info")

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_api)
    p2 = multiprocessing.Process(target=run_streamlit)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
