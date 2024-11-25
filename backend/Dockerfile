FROM python:3.13-slim

WORKDIR /backend
COPY . /backend/

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]