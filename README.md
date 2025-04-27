This project provides a Flask API that generates Python code based on text-based prompts from users. It utilizes the Codellama model to generate code based on user input.

Features
Flask-based web API

Python code generation using the Codellama model

Dynamic responses based on user-provided prompts

Easy deployment with Docker

Kubernetes deployment support

Usage
Requirements
Docker

Kubernetes (optional)

Ollama API

Running with Docker
After downloading the project files, you can run the project on Docker with the following commands:

Build the Docker image:

bash
Kopyala
Düzenle
docker build -t aysenur2763/flask-api .
Run the container:

bash
Kopyala
Düzenle
docker run -e OLLAMA_API_URL=http://host.docker.internal:11434 -p 5001:5000 aysenur2763/flask-api:latest
The API will be available at http://localhost:5000.

Running with Kubernetes
Deploy with Helm:

bash
Kopyala
Düzenle
helm install ai-code-assistant ./helm-chart
