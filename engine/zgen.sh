#!/bin/bash

echo "LIMPIAR Y CREAR MIGRATIONS" 
echo "BORRAR Y GENERAR NUEVA BASE DE DATOS"
echo "ACTUALIZAR BASES DE DATOS para el SITE_NAME = "$1
echo " --> debe estar incluido en la lista de websites/__init__.py"
echo
#---------------------------------------------------------------------
export NUM_ADMIN_SITE="0"
# export DJANGO_SUPERUSER_PASSWORD="_"$1

# habilitar al cliente mysql del equipo a una base de datos remota
# En el fichero
# /etc/mysql/mysql.conf.d/mysqld.cnf
# skip-external-locking --> descomentar si está comentada
# bind-address		= 127.0.0.1 --> comentar
# bind-address		= 0.0.0.0 --> añadir

echo "PASO 1: Borrar Migrations"
python delmigrat.py 1
echo "PASO 2: Crear makemigrations"
python manage.py $1 makemigrations
echo "PASO 3: Borrar Base de datos"
python zdbdelete.py $1
echo "PASO 4: Generar Base de datos"
python zdbcreate.py $1
echo "PASO 5: Realizar migrate en la nueva Base de datos"
python manage.py $1 migrate

# $ ./manage.py migrate
# $ ./manage.py migrate --database=[database no default]
#-----------------------
# echo "PASO 6: Crear superusuario"
# python manage.py $1 createsuperuser --username=$1 --email=$1"@multiges.net"
# python manage.py $1 runserver 0.0.0.0:8010



# si la bd es sqlite hay que dar permisos:
# sudo chmod 777 -r .....SITES_DATOS/$1/....
#python manage.py migrate --database=infotemp
#python manage.py migrate --database=webpublica



#----------------------
# CRONTAB
# ----------------------------
# service crond status
# python manage.py crontab add



# Librerias del sistema operativo para Pillow (Tratamiento imagenes)
#---------------------
# $ sudo apt-get install libjpeg-dev
# $ sudo apt-get install libpng-dev
# $ sudo apt-get install zlib1g-dev
# $ sudo apt-get install wkhtmltopdf ++++

# Librerias python necesarias:
# pip list --> para ver los paquetes instalados
# -------------------------------
# pip install docutils
# pip install mysqlclient
# pip install reportlab
# pip install Pillow
# pip install wagtail
# pip install pdfkit
# pip install openpyxl 

 