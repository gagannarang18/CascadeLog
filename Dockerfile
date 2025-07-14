FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc python3-dev nginx curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the port Cloud Run expects
ENV PORT 8080
EXPOSE 8080

CMD ["bash", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & uvicorn server:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
