FROM docker.io/debian:latest AS builder
RUN apt-get update && apt-get install -y wget && \
    wget --no-verbose --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=12RLN19-fkL-qRJ-eY6to4qN_7cZZD2no' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=12RLN19-fkL-qRJ-eY6to4qN_7cZZD2no" -O wikitext-103-raw.model-25.wv.pkl && rm -rf /tmp/cookies.txt

FROM docker.io/tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
COPY ./app requirements.txt /app/app/
COPY --from=builder wikitext-103-raw.model-25.wv.pkl /app/app/ml_model/
ENV MAX_WORKERS=1
RUN pip install -r /app/app/requirements.txt && \
    mkdir -p /app/app/ml_model
