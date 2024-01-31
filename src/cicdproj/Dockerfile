FROM python:3.10-alpine

WORKDIR /app

COPY requirements_build.txt .

RUN pip install --no-cache-dir -r requirements_build.txt

COPY src/cicdproj/ .
