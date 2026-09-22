# CARLA 0.9.15 Python client — run.sh selects linux/amd64.
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpng16-16 libjpeg62-turbo libtiff6 \
    && rm -rf /var/lib/apt/lists/*

# Pin client to the exact server version. Mismatched versions fail to connect.
RUN pip install --no-cache-dir carla==0.9.15 numpy

WORKDIR /app
COPY *.py ./
CMD ["python", "spawn_test.py"]
