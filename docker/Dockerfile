FROM --platform=linux/amd64 python:3.11.4-slim-buster as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates wget \
      gcc build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY ./requirements/ ./requirements/
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    rm -rf requirements && rm requirements.txt

COPY ./src/app ./app

EXPOSE 8017

CMD ["python", "-m", "uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8017"]
