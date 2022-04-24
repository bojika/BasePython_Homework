#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn topograph.wsgi:application --bind 0.0.0.0:8000 --access-logfile - --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "x-real-ip:%({x-real-ip}i)s" "host:%({host}i)s" "x-forwarded-for:%({x-forwarded-for}i)s" "origin:%({origin}i)s"'
