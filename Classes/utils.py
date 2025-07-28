import subprocess
import socket
import time
import logging
class Utilities:
    def __init__(self):
        pass
    
    def ensure_ollama_running(self,host="localhost", port=11434, timeout=10):
        logging.info("Starting Ollama Server")
        def is_running():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                return sock.connect_ex((host, port)) == 0

        if not is_running():
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            start = time.time()
            while time.time() - start < timeout:
                if is_running():
                    return
                time.sleep(0.2)
            raise RuntimeError("Ollama failed to start within the timeout window.")