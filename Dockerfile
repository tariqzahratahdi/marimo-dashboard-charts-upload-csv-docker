# Dockerfile for Back4app deployment

# Choose a slim version of Python for faster deployment builds
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your marimo application script
COPY app.py .

# Back4app routing needs the port exposed (typically 8080)
EXPOSE 8080

# Create a non-root user and switch to it
RUN useradd -m app_user
USER app_user

# Run marimo in app (read-only) mode bound to all network interfaces
CMD [ "marimo", "run", "app.py", "--host", "0.0.0.0", "-p", "8080" ]
