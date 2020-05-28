#!/bin/bash
cd /app/src
python manage.py migrate
python manage.py runserver --settings=eatery.docker_settings.py