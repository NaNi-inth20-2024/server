#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py runserver $SERVER_IP:$SERVER_PORT

exec "$@"