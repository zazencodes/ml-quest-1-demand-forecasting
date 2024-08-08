FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

