FROM docker.io/kalilinux/kali-rolling

ARG SYSTEM_DEPENDENCIES
ARG PYTHON_DEPENDENCIES
ARG SCENARIO_PATH
ENV ENTRYPOINT="$SCENARIO_PATH/scenario.py"

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates python3 curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get install -y $SYSTEM_DEPENDENCIES

WORKDIR nsak

COPY . .

RUN uv init && uv add $PYTHON_DEPENDENCIES

ENTRYPOINT exec uv run $ENTRYPOINT
