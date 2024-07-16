# syntax=docker/dockerfile:1
FROM python:3.12

LABEL name="Restaurant Backend"
LABEL description="Hosts the FastAPI backend of Restaurant"

WORKDIR /app

# Install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy server files
COPY . .

# Run server to accept all connections on port 80
EXPOSE 8000
#ENTRYPOINT ["uvicorn", "server.app:app"]
#CMD ["--host=127.0.0.1", "--port=80"]
CMD ["python", "main.py"]
