FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional: Create directories if needed
RUN mkdir -p /app/resources

EXPOSE 8000
EXPOSE 8501
