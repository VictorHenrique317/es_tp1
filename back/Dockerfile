# Use the official Python 3.9 Slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install necessary dependencies and faster-whisper
RUN apt-get update && apt-get install sqlite3 -y --no-install-recommends \
    curl \
    && pip install --no-cache-dir -U faster-whisper \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh 

# Install ollama model in the image
RUN ollama serve & \
    sleep 1 && \
    ollama pull llama3.2:1b

# Copy the application code
COPY . .
RUN pip install -r requirements.txt

# Install whisper model in the image
RUN python3 src/llms.py 

ENTRYPOINT ["sh", "-c"]

CMD ["ollama serve & PYTHONPATH=src uvicorn main:app --host 0.0.0.0 --port 80"]
