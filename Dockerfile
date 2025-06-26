FROM node:20 AS build-stage
RUN npm install -g pnpm

WORKDIR /app

COPY client/package.json client/pnpm-lock.yaml ./
RUN pnpm install

COPY client/ ./
RUN pnpm run build

FROM python:3.12
RUN apt-get update && apt-get install -y ffmpeg
RUN curl -LsSf https://astral.sh/uv/install.sh | sh 
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY api ./

WORKDIR /app/api

RUN uv sync

RUN mkdir client-dist
COPY --from=build-stage /app/dist /app/api/client-dist


ENTRYPOINT [ "uv", "run", "fastapi", "run", "main.py", "--port", "5677" ]

