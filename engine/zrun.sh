#!/bin/bash

echo "OJO!!! Necesita 3 parametros:  1 = SITE_NAME, 2 = puerto y 3 = NUM_ADMIN_SITE"
echo "EJECUTAR site_name "$1" en el puerto 801"$2" con NUM_ADMIN_SITE = "$3
# $1 = SITE_NAME --> debe estar incluido en la lista de websites/__init__.py
# $2 = NUM_ADMIN_SITE y ultimo dígito del puerto
export RUNSERVER=True
export NUM_ADMIN_SITE=$3
python manage.py $1 runserver 127.0.0.1:801$2
#--------------
# python manage.py $1 runserver 0.0.0.0:8000
# OJO!!! url para servir al front IP:8000/engine....


# EJEMPLOS DE USO:
#--------------------------
# . zrun.sh engine 0 1 -> http://127.0.0.1:8010/engine/
#                       en linux con DJANGO_SETTINGS_MODULE='engine.settings'
# ./zrun.sh engine 0 1 -> http://127.0.0.1:8010/engine/
#                       en mac con DJANGO_SETTINGS_MODULE='engine.settings'

# . zrun.sh [website]] 1 1 -> http://127.0.0.1:8011/[website]/
#                       en linux on DJANGO_SETTINGS_MODULE='engine.[website]].settings'
# ./zrun.sh [website]] 1 1 -> http://127.0.0.1:8011/[website]/
#                       en mac on DJANGO_SETTINGS_MODULE='engine.[website]].settings'
