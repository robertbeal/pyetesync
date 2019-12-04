FROM alpine:3.10.3
LABEL maintainer="github.com/robertbeal"

WORKDIR /app
COPY . /app

RUN apk add --no-cache --virtual=build-dependencies \
    alpine-sdk \
    libffi-dev \
    libressl-dev \
    python3-dev \
  && apk --no-cache add \
    libressl \
    python3 \
    py-tz \
  && python3 -m pip install --upgrade pip \
  && python3 -m pip install -r requirements.txt \
  && apk del --purge build-dependencies \
  && adduser -D -s /bin/false etesync \
  && chmod -R 500 /app \
  && chown -R etesync /app  

USER etesync
ENTRYPOINT ["python3", "backup.py"]
