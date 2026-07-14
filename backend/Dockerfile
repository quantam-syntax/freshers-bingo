FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PORT=5000
ENV FLASK_ENV=production

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "3", "--bind", "0.0.0.0:5000", "run:app"]
