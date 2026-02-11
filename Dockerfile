FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create memory.json with write permissions so the app doesn't crash
RUN echo "{}" > memory.json && chmod 666 memory.json

# Run the application on port 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "integrations.webhook_server:app"]