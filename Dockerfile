# Use an official Python runtime as a parent image
FROM python:3.12-slim

# 1. DO THIS FIRST: Run system-level commands as root to maximize caching
# Create the mount point immediately (system setup)
# RUN mkdir -p /var/run/secrets/kubernetes.io/serviceaccount

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container (dependency layer)
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (most frequent changes)
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run server.py when the container launches
CMD ["python", "server.py"]