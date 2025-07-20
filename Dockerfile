FROM python:3.13

RUN apt-get update

ENV DJANGO_ENV=DEVELOPMENT
WORKDIR /app

COPY . .

RUN python3 -m pip install poetry==2.1.3
RUN poetry config virtualenvs.create false
RUN poetry install --with utils --no-ansi --no-interaction
RUN ./manage.py migrate
RUN ./manage.py flush --noinput
RUN ./manage.py populate_db -s admin

EXPOSE 8001
CMD ["./manage.py", "runserver", "0.0.0.0:8001"]