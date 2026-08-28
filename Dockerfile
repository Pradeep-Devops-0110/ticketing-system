# Stage 1: Python App
FROM python:3.9-slim AS python-app

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]

# Stage 2: Jenkins with kubectl
FROM jenkins/jenkins:lts

USER root
RUN apt-get update && apt-get install -y docker.io curl \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

USER jenkins
