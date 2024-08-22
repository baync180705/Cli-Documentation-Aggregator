FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    gcc \
    pkg-config \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install -U google-generativeai
COPY . .
WORKDIR /app/src
CMD [ "../../bin/bash" ]