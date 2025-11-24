FROM docker.io/kalilinux/kali-rolling

# Python installieren # später dependencies in file auslagern
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    rm -rf /var/lib/apt/lists/* \

WORKDIR src

# copy project
COPY . src

# Standard-Entry: dein Scenario
CMD ["python3", "/src/scenarios/test-scenario/scenario.py"]