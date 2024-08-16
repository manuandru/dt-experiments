FROM ubuntu:22.04 AS builder

RUN apt update && apt install -y gettext
WORKDIR /app
COPY . /app
RUN ./build-env.sh

### STAGE RUNTIME ###

FROM python:3.12-slim

RUN apt update && apt install -y jq curl
WORKDIR /app

COPY --from=builder /app/connection/javascript-mapper.js \
    /app/connection/connection-provisioner.sh \
    /app/thing/requirements.txt \
    /app/thing/thing-description.json \
    /app/thing/thing-provisioner.py \
    /app/start.sh \
    /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "./start.sh" ]
