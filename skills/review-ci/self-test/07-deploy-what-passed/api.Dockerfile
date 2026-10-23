FROM python:3.14-slim@sha256:0f9a5c1e1b0d9b6c3e6c6d2b6a7b4f3e8c2d1a0f9e8d7c6b5a4f3e2d1c0b9a8f
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY src/ ./src/
CMD ["python3", "-m", "tally.api"]
