FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    git fish \
    ffmpeg \
    nodejs npm curl \
    python3 python3-pip pipx \
    && npm install -g n \
    && n stable \
    && npm install -g pnpm pyright

WORKDIR /app

RUN usermod -l developer ubuntu && \
    groupmod -n developer ubuntu && \
    usermod -d /home/developer -m developer && \
    chsh -s /usr/bin/fish developer

USER developer

RUN fish -c "echo Fish shell initialized"

COPY ./config.fish /home/developer/.config/fish/config.fish

RUN pipx install uv

ENV PATH="/home/developer/.local/bin:${PATH}"