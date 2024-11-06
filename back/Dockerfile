# Use the official Python 3.10 Slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install necessary dependencies, curl, supervisor, and Poetry
RUN apt-get update && apt-get install sqlite3 -y --no-install-recommends \
    curl \
    supervisor \
    && pip install poetry \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh 

# Copy the application code
COPY . /app

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false
RUN poetry install
 
# Copy supervisor configuration file
COPY ./supervisord.conf /etc/supervisord.conf

# Expose the necessary port
EXPOSE 80

# Set the entry point to use supervisor to manage both processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
