#!/bin/bash

echo "collecstatic para websites dj-engine en la subcarpeta "$1"_static":
echo "SITES_DATOS/"$1"/"$1"_static"
echo "Este comando copia todas las carpetas y ficheros static del sitio "$1
echo "en la carpeta definida por las variables definidas en su settings: "

export SITE_NAME=$1
python manage.py $1 collectstatic
