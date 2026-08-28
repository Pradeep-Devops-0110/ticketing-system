# Base Image: Python 3.9
FROM python:3.9-slim

# Set Working Directory
WORKDIR /app

# Copy Requirements and Install Dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy All Project Files
COPY . .

# Expose Port 5000
EXPOSE 5000

# Run Application
CMD ["python", "run.py"]