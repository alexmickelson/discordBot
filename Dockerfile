FROM node:20 AS build-stage
RUN npm install -g pnpm

WORKDIR /app

COPY client/package.json client/pnpm-lock.yaml ./
RUN pnpm install

COPY client/ ./
RUN pnpm run build

FROM python:3.12
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY main.py main.py
RUN mkdir songs

RUN mkdir client-dist
COPY --from=build-stage /app/dist /client-dist

RUN curl -LsSf https://astral.sh/uv/install.sh | sh 

ENV PATH="/root/.local/bin:${PATH}"

ENTRYPOINT [ "uv", "run", "fastapi", "run", "main.py", "--port", "5677" ]

