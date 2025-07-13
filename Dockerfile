FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all files EXCEPT .env (we'll mount it separately)
COPY . .

# Create directory for outputs
RUN mkdir -p /app/resources

EXPOSE 8000
EXPOSE 8501

CMD ["python", "run.py"]