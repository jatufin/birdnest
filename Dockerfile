# Base image
FROM python:3.8

# MAINTAINER of the Dockerfile
MAINTAINER jatufin

# Working directory inside the app
WORKDIR /usr/src/app

# Copy dependency list to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all application files
COPY . .

# Expose port
EXPOSE 5000

# Launch the app
ENTRYPOINT python -m flask --app src/app.py run --host 0.0.0.0