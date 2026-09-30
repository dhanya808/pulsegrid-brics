"""
PulseGrid BRICS - One-Click Application Launcher
Runs the FastAPI server with live interactive frontend on http://localhost:8000
"""
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import uvicorn

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    print("=" * 72)
    print("[*] Starting PulseGrid BRICS - Federated Health Resource Grid")
    print("[*] Dashboard URL:  http://localhost:8000")
    print("[*] Pitch Deck URL: http://localhost:8000/pitch")
    print("[*] API Swagger:    http://localhost:8000/docs")
    print("=" * 72)
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
