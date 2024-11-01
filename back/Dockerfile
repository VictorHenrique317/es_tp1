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

# Install model in the image
RUN ollama serve & \
    sleep 1 && \
    ollama pull llama3.2:1b

# Copy the application code
COPY . .
RUN pip install -r requirements.txt
#RUN python3 models.py # load the model in the image

ENTRYPOINT ["sh", "-c"]

#CMD ["ollama serve & python3 run.py"]
