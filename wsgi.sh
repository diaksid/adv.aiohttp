#! /bin/bash

source /var/venv/bin/activate;
exec   gunicorn app.wsgi:app --config wsgi.py
