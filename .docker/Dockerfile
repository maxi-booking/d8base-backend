FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y gettext sqlite3 libsqlite3-dev libpq-dev binutils libproj-dev gdal-bin

WORKDIR /usr/src/app
COPY ./setup.py ./README.md ./
COPY ./requirements/dev.txt ./requirements/
RUN pip install -e .
RUN pip install --no-cache-dir -r ./requirements/dev.txt

COPY . .