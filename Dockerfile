FROM python:3.11-slim

WORKDIR /app

# Install Tesseract and its dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for ChromeDriver binary path
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV DATABASE_URL='mongodb+srv://user:user6atharva@cluster0.3r8f5tw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ENV SETTINGS_FOR_TESSERACT='--oem 3 --psm 6 outputbase page'

# Copy ChromeDriver binary to the specified path in the Docker image
COPY chromedriver-linux64/chromedriver $CHROMEDRIVER_PATH

# Copy the rest of the application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Set command to run the FastAPI application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
