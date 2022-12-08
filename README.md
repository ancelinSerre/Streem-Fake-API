# Streem exercise

A simple API on which energy producers can upload their meter readings in order to obtain invoices.
A sqlite database is already included in this repository to allow you to test the different routes.

## Quick start

### With a Python virtual environment

Make sure you have a Python version >= 3.10.

```bash
python --version
```

Create a new virtual environment:

```bash
python -m venv .env
# For windows
.env/Scripts/activate 
# For linux
source .env/bin/activate
```

Install dependencies:

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Start the project:

```bash
cd src/
uvicorn app:app --port 8000
```

### With Docker

Build the Docker image:

```bash
docker build -t streem-fake-api:1.0.0 .
```

Start a new container for the API:

```bash
docker run -d --name streem-container -p 8000:8000 streem-fake-api:1.0.0
```

Access Swagger and discover the API:

```txt
http://127.0.0.1/docs
```
