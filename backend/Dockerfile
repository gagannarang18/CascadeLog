# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose the port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
