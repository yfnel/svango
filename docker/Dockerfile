FROM python:3.13

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get install -y python3-dev build-essential libldap2-dev libsasl2-dev ldap-utils

ENV DJANGO_ENV=DEVELOPMENT
WORKDIR /app

COPY .. .

RUN python3 -m pip install poetry==2.1.3
RUN poetry config virtualenvs.create false
RUN poetry install --with utils --with stage --no-ansi --no-interaction
RUN chmod +x /app/docker/entrypoints/*