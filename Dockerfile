FROM alpine:3.10

RUN apk add --no-cache \
	bash python zip

COPY entrypoint.sh /entrypoint.sh
COPY extract_name.py /extract_name.py

ENTRYPOINT ["/entrypoint.sh"]
