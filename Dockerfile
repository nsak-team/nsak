FROM docker.io/kalilinux/kali-rolling

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates python3 curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR nsak
COPY . .

ARG SYSTEM_DEPENDENCIES
ARG PYTHON_DEPENDENCIES
ARG SCENARIO
ENV ENTRYPOINT="nsak scenario execute --name $SCENARIO"
ENV NSAK_LIBRARY_PATH="lib/"

RUN apt-get install -y $SYSTEM_DEPENDENCIES

RUN uv sync && \
    uv add $PYTHON_DEPENDENCIES && \
    uv pip install . && \
    uv build && \
    uv tool install dist/nsak-0.1.0-py3-none-any.whl

CMD $ENTRYPOINT
