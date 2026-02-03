# Minimal FastAPI Application

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
```

## Running the Application

```bash
.venv/bin/uvicorn src.app:app --reload
```

Or use the VS Code debugger to run the application.
