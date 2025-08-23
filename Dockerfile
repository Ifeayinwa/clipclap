# Use official Python image (Python 3.10 is a stable choice)
FROM python:3.10-slim

# Set environment variables to prevent writing .pyc files and to have unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000  

# Set working directory
WORKDIR /app

# Install system dependencies required for psycopg2 and build tools
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Create a non-root user (optional for security)
RUN adduser --disabled-password myuser
USER myuser

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (the container will use this port)
EXPOSE 8000

# Start the Django app using Gunicorn, binding to all interfaces on the specified port
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:$PORT"]
