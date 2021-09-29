# -*- coding: utf-8 -*-

import os, sys, re
from shutil import rmtree
from importlib import import_module
from django.conf import settings
from django.db.utils import load_backend
# from django.contrib import messages
# from django.utils import timezone

#-----------------------
# BASES DE DATOS
#------------------------

# dbcreate
# dbdelete
# dbsite_generate <-- zgen.py
# dbsite_delete <-- zdel.py
# delete_migrations
# db_backup
# db_restore

def get_connection(db):
	# import pdb; pdb.set_trace()
	name = db['NAME']
	engine = db['ENGINE'].split('.')[-1]
	host = db.get('HOST','')
	port = db.get('PORT','')
	user = db.get('USER','')
	password = db.get('PASSWORD', '')
	#---------------------
	if engine == 'firebird':
		import fdb
		dsn = '%s/%s:%s' % (host, port, name)
		conn = fdb.connect(dsn=dsn, user=user, password=password)
	else:
		Backend = load_backend(db['ENGINE']).Database
		conn = Backend.connect(name)
		# conn.close()
		print("La base de datos de %s YA existe." % name)
	return conn


def execute_consulta(db, consulta):
	# import pdb; pdb.set_trace()
	conn = get_connection(db)
	cursor = conn.cursor()
	cursor.execute(consulta)
	datos = cursor.fetchall()
	cursor.close()
	conn.close()    
	return datos






#------------------------------
def dbcreate(db):
	"""
	 db es un diccionario con el mismo formato que en setting.DATABASES
	"""
	name = db['NAME']
	engine = db['ENGINE'].split('.')[-1]
	user = db.get('USER','')
	password = db.get('PASSWORD', '')
	print('%s %s %s %s' % (name, engine, user, password))
	#-----------
	# Comprobar si existe -- Load_Backend ...
	if engine == 'sqlite3':
		message = "Motor sqlite: No hay que crear base de datos para %s" % name
		level = 25
		print('%s %s' % (user, password))
	#-------------------------
	# elif engine == 'mysql':
	# 	# import pdb; pdb.set_trace()
	# 	import MySQLdb
	# 	user_full = "'%s'@'localhost'" % user
	# 	# user_full = "'%s'@'*'" % user
	# 	password_full = "'%s'" % password
	# 	con = MySQLdb.connect(user="root", passwd=password)
	# 	cur = con.cursor()
	# 	cur.execute('create database %s character set utf8;' % name)
	# 	cur.execute("CREATE USER %s IDENTIFIED BY %s;" % (user_full, password_full))
	# 	cur.execute("GRANT ALL PRIVILEGES ON %s.* TO %s IDENTIFIED BY %s WITH GRANT OPTION;" % (
	# 					name, user_full, password_full))
	# 	cur.close 
	# 	con.close()
	# 	message = "Base de Datos %s creada" % name
	# 	level = 25 # messages.SUCCESS
		
	# elif engine == 'postgresql_psycopg2':
	# 	import psycopg2
	# 	# con = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password=''")
	# 	con = psycopg2.connect(user='root', password=passw_motor_db)
	# 	cur = con.cursor()
	# 	cur.execute('CREATE DATABASE %s ENCODING UTF8;' % name)
	# 	cur.execute("CREATE USER %s PASSWORD '%s';" % (user, password))
	# 	cur.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s WITH GRANT OPTION;" % (
	# 	                        name, user))
	# 	cur.close()
	# 	con.close()
	# 	message = "Base de Datos %s creada" % name
	# 	level = 25 # messages.SUCCESS

	elif engine == 'oracle':    
		message = "Motor %s no soportado en esta version" % engine
		level = 40

	elif engine == 'mongoDB':    
		message = "Motor %s no soportado en esta version" % engine
		level = 40
	else:
		message = "Motor %s no soportado en esta version" % engine
		level = 40

	return message, level
#-------------------------------

#----------------------------------
# Generar base de datos y carpetas de datos para un website
#--------------------------------------
def dbsite_generate(db=None):
	#------------------
	# Crear carpetas de datos
	#---------------------
	carpeta = os.path.join(settings.DATA_ROOT)
	if not os.path.isdir(carpeta):
		os.system('mkdir -p %s' % carpeta)
		print("CREADA CARPETA DATOS: %s" % carpeta)

	#-----------------
	# Crear la base de datos
	#-------------------------
	if db:
		message, level = dbcreate(db) 
		print("CREADA BASE DE DATOS: %s %s %s %s" % (db, db.get['NAME'], message, level))
	else:
		for key, db in settings.DATABASES.items():
			message, level = dbcreate(db) # , PASSW_MOTOR_DB)
			print("CREADA BASE DE DATOS: %s %s %s %s" % (key, db.get('NAME',''), message, level))
	return


def dbdelete(db):
	"""
	 db es un diccionario con el mismo formato que en setting.DATABASES
	"""
	name = db['NAME']
	engine = db['ENGINE'].split('.')[-1]
	host = db.get('HOST','')
	user = db.get('USER','')
	password = db.get('PASSWORD', '')
	# print('%s %s %s %s %s' % (name, engine, host, user, password))
	#-----------
	# import pdb; pdb.set_trace()
	if engine == 'sqlite3':
		message = "Motor sqlite: Se borra el fichero %s" % name
		os.system('rm %s' % name)
		# carpeta = os.path.dirname(name)
		# os.system('rm %s' % carpeta)
		level = 25
	#-------------------------n
	# elif engine == 'mysql':
	# 	#---------------
	# 	cmd = "mysql -h %s -u root --password=%s -e 'DROP %s'" % (host, password, name)
	# 	x_cmd = "mysqladmin --user=%s --password=%s --force drop %s" % (
	# 					db['USER'], db['PASSWORD'], db['NAME'])
	# 	try:
	# 		os.system(cmd)
	# 		message = "Bases de Datos %s borrada" % name
	# 		level = messages.SUCCESS
	# 	except:
	# 		message = "NO SE PUEDE BORRAR LA BASE DE DATOS"
	# 		level = messages.ERROR

	elif engine == 'postgresql_psycopg2':    
		message = "Motor %s no soportado en esta version" % engine
		level = 40
	elif engine == 'oracle':    
		message = "Motor %s no soportado en esta version" % engine
		level = 40

	elif engine == 'mongoDB':    
		message = "Motor %s no soportado en esta version" % engine
		level = 40
	else:
		message = "Motor %s no soportado en esta version" % engine
		level = 40
	# print("%s %s" % (name, message))
	return message, level

def dbsite_delete(db=None):
	#------------------
	# Borrar carpetas de datos, borrará también las bases de datos sqlite3
	#---------------------
	# carpeta = os.path.join(settings.DATA_ROOT, 'fixtures')
	carpeta = os.path.join(settings.DATA_ROOT)
	# import pdb; pdb.set_trace()
	if os.path.isdir(carpeta):
		rmtree(carpeta)
		# os.system('remove -r %s' % carpeta)
		print("BORRADA CARPETA DATOS: %s" % carpeta)
	#-----------------
	# Eliminar la base de datos
	#-------------------------
	# import pdb; pdb.set_trace()

	#-------------------------------
	if db: # 'default'
		lista_dbs = [{'default': db}]
	else:
		lista_dbs = settings.DATABASES.items()
	if lista_dbs: 
		for key, db in lista_dbs:
			engine = db['ENGINE'].split('.')[-1]
			if engine != 'sqlite3':
				message, level = dbdelete(db)
				print("BORRADA %s %s %s" % (db, message, level))
			else:
				print("Ya fue BORRADA %s" % (db['NAME']))
	return

def delete_migrations(desde='2', dir_to_search='.'):
	for dirpath, dirnames, filenames in os.walk(dir_to_search):
		for di in dirnames:
			if (di == 'migrations'):
				dpath = os.path.join(dirpath, di)
				for dirpath, dirnames, filenames in os.walk(dpath):
					for fi in filenames:
						if (re.match(r'0\d{3}_.*\.py', fi)):
							if fi > '000%s_' % desde:
								fpath = os.path.join(dirpath, fi)
								print('About to delete', fpath)
								os.remove(fpath)
								# TODO !!! incluir el borrado de los registros de la tabla
	return


def db_backup(db=None):
	return

def db_restore(db=None):
	return