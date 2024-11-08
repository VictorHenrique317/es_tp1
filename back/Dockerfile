# Use the official Python 3.10 Slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install necessary dependencies, curl, supervisor, and Poetry
RUN apt-get update && apt-get install sqlite3 -y --no-install-recommends \
    curl \
    && pip install poetry \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh 

# Install llama in the image
RUN ollama serve & \
   sleep 1 && \
   ollama pull llama3.2:1b
 
# Copy the application code
COPY . /app

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

RUN python3 src/load_whisper.py

# Expose the necessary port
EXPOSE 80

# Starts the FastAPI server
CMD ollama serve &\
    sleep 1 &&\
    ollama  create summarizer -f ./Modelfile &&\
    uvicorn src.main:app --host 0.0.0.0 --port 80
