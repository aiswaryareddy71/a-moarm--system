FROM python:3.9-slim
WORKDIR /app
# Install system dependencies for psycopg2 and AI processing [cite: 385, 408]
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run on port 8000 for Docker mapping [cite: 33]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]