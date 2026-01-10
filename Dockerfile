FROM docker.io/kalilinux/kali-rolling as BASE_IMAGE

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates python3 python3-dev curl iproute2


RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR nsak
COPY . .

FROM BASE_IMAGE

ARG SYSTEM_DEPENDENCIES
ARG PYTHON_DEPENDENCIES
ARG SCENARIO
# Convert build args to env variables, to leverage the caching mechanism
ENV SYSTEM_DEPENDENCIES=${SYSTEM_DEPENDENCIES}
ENV PYTHON_DEPENDENCIES=${PYTHON_DEPENDENCIES}
ENV SCENARIO=${SCENARIO}
ENV ENTRYPOINT="nsak scenario execute $SCENARIO"
ENV NSAK_LIBRARY_PATH="lib/"

RUN apt-get install -y $SYSTEM_DEPENDENCIES

RUN uv sync && \
    if [ -n "$PYTHON_DEPENDENCIES" ]; then uv add $PYTHON_DEPENDENCIES; fi && \
    uv pip install . && \
    uv build && \
    uv tool install dist/nsak-0.1.0-py3-none-any.whl

CMD $ENTRYPOINT
