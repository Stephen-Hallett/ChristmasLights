FROM ubuntu:oracular

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

WORKDIR /data

COPY schema.sql /data/
COPY entrypoint.sh /data/
RUN chmod a+rx /data/entrypoint.sh

ENTRYPOINT ["/data/entrypoint.sh"]