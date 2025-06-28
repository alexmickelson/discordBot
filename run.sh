#!/bin/bash

git pull

docker pull node:20
docker pull python:3.12

docker compose up --build -d
docker compose restart mcpo