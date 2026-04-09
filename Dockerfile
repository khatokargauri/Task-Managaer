# Use Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy files
COPY main.py index.html .

# Install dependencies
RUN pip install fastapi uvicorn

# Expose port
EXPOSE 8000

# Run app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]