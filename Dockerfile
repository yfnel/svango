FROM python:3.13

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get install -y python3-dev build-essential libldap2-dev libsasl2-dev ldap-utils

ENV DJANGO_ENV=DEVELOPMENT
WORKDIR /app

COPY . .

RUN python3 -m pip install poetry==2.1.3
RUN poetry config virtualenvs.create false
RUN poetry install --with utils --no-ansi --no-interaction
RUN ./manage.py migrate
RUN ./manage.py collectstatic --noinput
RUN ./manage.py compilemessages

EXPOSE 8000
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]