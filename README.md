# Trackmind - Interim Prototype

## Requirements

- Python 3
- pip
- Web browser

## Installation

Extract the ZIP file and open a terminal in the Trackmind project directory.

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### 1. Start the backend

From the project directory, with the virtual environment activated, run:

```bash
uvicorn backend.main:app --reload
```

### 2. Start the frontend

Open a second terminal in the project directory and run:

```bash
python3 -m http.server 5500
```

On Windows, use `python` instead of `python3` if required.

### 3. Access Trackmind

Open the following URL in your web browser:

http://127.0.0.1:5500/index.html

Upload an aerial circuit image to view the automatically detected circuit boundaries.

Both terminals must remain running while using the application.

To stop either server, press `Ctrl + C` in its terminal.
