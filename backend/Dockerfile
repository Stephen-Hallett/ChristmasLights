FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

ADD . /backend

WORKDIR /backend
RUN uv sync --locked

EXPOSE 81

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "81"]