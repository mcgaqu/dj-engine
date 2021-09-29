#!/bin/bash

echo "EJECUTAR INSTALACION "$1""
echo "en el puerto 801"$2"" 
echo "con NUM_ADMIN_SITE = "$3""
# $1 = SITE_NAME  --> debe estar incluido en la lista de websites/__init__.py
# $2 = ultimo dígito del puerto
# $3 = NUM_ADMIN_SITE
export RUNSERVER=True
export NUM_ADMIN_SITE=$3
# python manage.py $1 runserver 127.0.0.1:801$2 
#--------------
python manage.py $1 runserver 0.0.0.0:809$2
# OJO!!! url para servir al front IP:8000/[site name]....


# EJEMPLOS DE USO:
#--------------------------
# . zrun0.sh engine 0 -> http://0.0.0.0:8090/engine/
#                       con DJANGO_SETTINGS_MODULE='engine.settings'

# . zrun0.sh site02 1 -> http://127.0.0.1:8091/site02/
#                       con DJANGO_SETTINGS_MODULE='websites.site02.settings'

# . zrun0.sh site01 2 -> http://192.168.1.19:8092/site012/
#                       con DJANGO_SETTINGS_MODULE='websites.site01.settings'
