FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system deps including PortAudio for microphone support
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    libportaudio2 \
    libasound2-dev \
    libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

ADD . /client

WORKDIR /client

# Prefer uv-managed dependencies if pyproject+lock present, otherwise fall back to requirements.txt
RUN uv sync --locked

ENV PYTHONUNBUFFERED=1

# Default runtime
CMD ["uv", "run", "python", "ChristmasClient.py"]