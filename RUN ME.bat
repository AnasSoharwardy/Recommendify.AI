REM Run FastAPI backend
start cmd /k "uvicorn main:app --reload"

REM Run Streamlit frontend
start cmd /k "streamlit run app.py"

