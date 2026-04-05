# Use Python base image
FROM python:3.10-slim

# Install system dependencies (IMPORTANT for pytesseract)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Expose port
EXPOSE 10000

# Start app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]