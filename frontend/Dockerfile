FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

ADD . /frontend

WORKDIR /frontend
RUN uv sync --locked

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501"]
