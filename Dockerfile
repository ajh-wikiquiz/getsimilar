# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * Install wget to download inference model
# * Update pip to support bdist_wheel
FROM docker.io/debian:buster-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev wget && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    wget --no-verbose --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=12RLN19-fkL-qRJ-eY6to4qN_7cZZD2no' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=12RLN19-fkL-qRJ-eY6to4qN_7cZZD2no" -O wikitext-103-raw.model-25.wv.pkl && rm -rf /tmp/cookies.txt

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy and move files into place
FROM build-venv AS move
COPY ./app /app
RUN mkdir -p /app/ml_model && \
    mv wikitext-103-raw.model-25.wv.pkl /app/ml_model

# Copy the the necessary files into the distroless image
FROM gcr.io/distroless/python3-debian10 AS pre
COPY --from=move /venv /venv
COPY --from=move /app /app

# Basically squashing the COPY commands in the final image
FROM gcr.io/distroless/python3-debian10
COPY --from=pre / /
ENV GUNICORN_CMD_ARGS="--workers=1 --worker-class=uvicorn.workers.UvicornWorker"
ENTRYPOINT ["/venv/bin/gunicorn", "app.main:app"]
