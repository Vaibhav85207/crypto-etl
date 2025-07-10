FROM python:3.11-slim

# Set the working directoryWORKDIR /app
run apt-get update && apt-get install -y ca-certificates 
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY transform.py .
CMD ["python", "transform.py"]   