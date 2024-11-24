FROM ubuntu:oracular

RUN apt-get -y update
RUN apt-get -y upgrade

WORKDIR /frontend
COPY . /frontend/

RUN pip install -r requirements.txt
