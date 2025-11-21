FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (app.py + parquet + others)
COPY . .

# Hugging Face Spaces expects the app on port 7860
EXPOSE 7860

# Run Dash via gunicorn, binding to 0.0.0.0:7860
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:7860"]
