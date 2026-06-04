# Build Stage
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    clang \
    libclang-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir atheris

ADD . /src
WORKDIR /src
RUN SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1 python3 -m pip install .

CMD ["/src/mayhem/fuzz_parse.py"]
