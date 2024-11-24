FROM python:3.13-slim

WORKDIR /frontend
COPY . /frontend/

RUN ls -la /frontend

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]
