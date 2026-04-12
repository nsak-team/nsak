FROM docker.io/kalilinux/kali-rolling as base_image

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates python3 python3-dev curl wget iproute2 arp-scan dsniff iptables \
    openssh-client dnsutils nmap smbclient ldap-utils netcat-openbsd snmp vim iputils-* sshpass autossh git

# NVM environment variables
ENV NVM_DIR=/root/.nvm
ENV NODE_VERSION=22

# Install nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Install Node via nvm
RUN bash -c "source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm use $NODE_VERSION && \
    nvm alias default $NODE_VERSION"

WORKDIR nsak
RUN git clone https://github.com/langchain-ai/agent-chat-ui.git
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY . .

FROM base_image

ARG SYSTEM_DEPENDENCIES
ARG PYTHON_DEPENDENCIES
ARG SCENARIO
# Convert build args to env variables, to leverage the caching mechanism
ENV SYSTEM_DEPENDENCIES=${SYSTEM_DEPENDENCIES}
ENV PYTHON_DEPENDENCIES=${PYTHON_DEPENDENCIES}
ENV SCENARIO=${SCENARIO}
ENV NSAK_ENV_FILE=".env"
ENV NSAK_RUN_PATH="run/"
ENV NSAK_LIBRARY_PATH="lib/"

RUN apt-get install -y $SYSTEM_DEPENDENCIES

RUN uv sync && \
    if [ -n "$PYTHON_DEPENDENCIES" ]; then uv add $PYTHON_DEPENDENCIES; fi && \
    uv pip install . && \
    uv build && \
    uv tool install dist/nsak-0.1.0-py3-none-any.whl

# drawio-mcp-server
ENTRYPOINT ["nsak", "scenario", "execute"]
