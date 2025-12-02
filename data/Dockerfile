FROM alpine:3.19

RUN apk add --no-cache sqlite

WORKDIR /data

COPY schema.sql /data/
COPY entrypoint.sh /data/
RUN chmod a+rx /data/entrypoint.sh

ENTRYPOINT ["/data/entrypoint.sh"]