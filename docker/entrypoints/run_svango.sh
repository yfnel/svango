#!/bin/bash
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages
uwsgi --http :8000 --module mate.wsgi