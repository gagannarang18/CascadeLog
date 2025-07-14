FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Use $PORT for Render dynamic port binding
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=${PORT}"]
