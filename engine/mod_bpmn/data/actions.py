
# ejecutar operaciones sobre bases de datos
#    a) comando systema: mysql, msqladmin, ...
#-----------------------
# copia seguridad
# recuperacion copia seguridad
### crear base de datos
### borrar base de datos

# action del modelo Dbquery
# ejecutar operaciones CRUD sobre bases de datos
#    b) connection
# consultas
# modificaciones
# inserciones
# borrados

def get_app_arcos():
	return []
"""
from mod_admin.databases.dbgen import (
	dbcreate,
	dbdelete,
	dbsite_generate,
	dbsite_delete,
	db_backup,
	db_restore,
	delete_migrations
)
 
def ac_dbsite_generate(modeladmin, request, queryset):
	return

def ac_dbsite_generate(modeladmin, request, queryset):
	return

def ac_dbsite_generate(modeladmin, request, queryset):
	return

cmd = "CREATE DATABASE <dbname> CHARACTER SET utf8_unicode_ci;"
# borrar base de datos
cmd = "DROP DATABASE;"
# crear tabla
# ...

def get_connection(db):
    name = db['NAME']
    engine = db['ENGINE'].split('.')[-1]
    host = db.get('HOST','')
    user = db.get('USER','')
    password = db.get('PASSWORD', '')
    #---------------------
    if True:
        Backend = load_backend(db['ENGINE']).Database
        conn = Backend.connect(db=db['NAME'],
                                    user=db['USER'],
                                    passwd=db['PASSWORD'],
                                    use_unicode=True)
        # conn.close()
        mensaje = _("La base de datos de %s YA existe." % obj.username)
        return conn

    else:
        if engine == 'sqlite':
            conn = None
        elif engine == 'mysql':
            import MySQLdb
            # passwd = "%s_%s" % (db1.split('_')[1], db1.split('_')[0])
            conn = MySQLdb.connect(user=user, db=name,
                                passwd=password, host=host, #  host='localhost',
                                use_unicode=True
                                )
            conn.set_character_set('utf8')
        elif engine == 'postgresql':
            conn = None
        elif engine == 'oracle':
            conn = None
        elif engine == 'mongodb':
            conn = None
        else:
            conn = None
        return conn



def run_dbquery(db, dbquery):
    #-----------------------
    # dbquery = Instruccion en el lenguaje de base de datos de que se trate
    # de momento en SQLITE
    #----------------------
    try:    
        conn = get_conection(db)
        cursor = conn.cursor()
        #------------------------
        # si es una consulta de escritura
        transaction.commit_unless_managed()
        cursor.execute(dbquery)
        #------------------------
        cursor.close()
        conn.close()
        message = "Exito"
        level = 25
    except:
        message = "Error"
        level = 40
    return (message, level)           


def ac_run_dbquery(modeladmin, request, queryset):
	for obj in queryset:
		if not obj.bloqueado:
			db = obj.db.config
			dbquery = obj.name
			message, level = run_dbquery(db, dbquery)
			message = "Dbquery %s: " % message
			modeladmin.message_user(request, message, level=level)
		else:
			mensaje = _("%s: bloqueado. No se inicia base de datos") % (obj.alias)
			modeladmin.message_user(request, mensaje, level=messages.ERROR)
	return
ac_run_dbquery.short_description = "Ejecutar Operación sobre Base de Datos"

#===========================0

def init_database(modeladmin, request, obj):
	if True:
		mensaje = "Hay que eliminar la base de datos iris_%s" % obj.alias
		modeladmin.message_user(request, mensaje, level = messages.WARNING)
	else:
		#-------------------------
		# No ACTIVO: Completar cuando haga falta
		#-----------------------------
		motor = db['ENGINE'].split('.')[-1]
		if motor == 'sqlite3':
			#-----
			# Borrar si existe
			#---
			nombre = db['NAME']
			if obj.userinstalx.reemplaza and os.path.isfile(nombre):
				cmd = "move %s_%s" % (nombre, datetime.datetime.now().strftime("%Y%M%D"))
				os.system(cmd)
				# obj.bloqueado = True
				obj.save()
				mensaje = "Base de datos %s eliminada" % nombre
				modeladmin.message_user(request, mensaje, level = messages.WARNING)
			mensaje = "Motor sqlite: No hay que crear base de datos para %s" % nombre
			modeladmin.message_user(request, mensaje, level=messages.WARNING)
		else:
			Backend = load_backend(db['ENGINE']).Database
			# try:
			# import pdb; pdb.set_trace()
			if True:
				conexion = Backend.connect(db=db['NAME'],
										   user=db['USER'],
										   passwd=db['PASSWORD'],
										   use_unicode=True)
				conexion.close()
				mensaje = _("La base de datos de %s YA existe." % obj.username)
				modeladmin.message_user(request, mensaje, level = messages.WARNING)
				if obj.userinstalx.reemplaza:
					mensaje, level = crear_database(db, borrar=True)
					# obj.bloqueado = True
					obj.save()
					modeladmin.message_user(request, mensaje, level=level)    
			else: #except Exception:
				mensaje = _("La base de datos de %s no existe. Se crea." % obj.username)
				modeladmin.message_user(request, mensaje)
				# borrar = (obj.userinstalx.reemplaza and not obj.userinstalx.bloqueado)
				mensaje, level = crear_database(db)
				modeladmin.message_user(request, mensaje, level=level)                
	return


def ac_dbsite_generate(modeladmin, request, queryset):
from mod_admin.databases.dbgen import dbsite_generate
for obj in queryset:
	if not obj.bloqueado:
		dbsite_generate(modeladmin, request, obj)
		# modeladmin.message_user(request, mensaje, level=level)
	else:
		mensaje = _("%s: bloqueado. No se inicia base de datos") % (obj.alias)
		modeladmin.message_user(request, mensaje, level=messages.ERROR)
return
ac_dbsite_generate.short_description = "2. Crear Base de Datos"

#--------------------
# Pendiente de revision
#---------------------------

def recuperar_backup(modeladmin, request, obj):
    # import pdb; pdb.set_trace()
    if not hasattr(obj, 'userinstalx'):
        mensaje = _("%s: no tiene Instalación") % (obj.username)
        modeladmin.message_user(request, mensaje, level=messages.ERROR)
        return
    elif obj.userinstalx.bloqueado: # not self.db_crear:
        mensaje = _("%s: bloqueado. No se puede recuperar backup") % (obj.username)
        modeladmin.message_user(request, mensaje, level=messages.ERROR)
        return
    #-------------------------------
    db = json.loads(obj.userinstalx.database)
    motor_db = db['ENGINE'].split('.')[-1]
    ysitio = obj.userinstalx.ysitio
    origen = ysitio.kind
    if not origen:
        mensaje = "No hay archivo origen a recuperar"
        modeladmin.message_user(request, mensaje, level=messages.WARNING) 
        return
    tipo = origen.split('.')[-1]
    # import pdb; pdb.set_trace()
    if tipo in ('sqlite3', 'postgresql_psycopg2', 'mysql', 'oracle'):
        if tipo != motor_db:
            mensaje = "El modor de la base de datos no coincide con el sitio elegido"
            modeladmin.message_user(request, mensaje, level=messages.ERROR) 
        else:
            if tipo == 'sqlite3':
                #fichero_origen = os.path.join(
                #    os.path.dirname(settings.BASE_DIR), 
                #    ysitio.project, # multiges
                #    'ysitios', 
                #    ysitio.nick, # aplicacion (ysitio)
                #    origen)
                db_name = db['NAME']    
                cmd = "cp %s %s" % (origen, db_name)
                os.system(cmd)
                mensaje = _("Backup %s recoverded" % origen)
            elif tipo == 'mysql':
                cmd = "mysql --user=%s --password=%s %s < %s" % (
                    db['USER'], db['PASSWORD'], db['NAME'], origen)
                os.system(cmd)
                mensaje = _("Backup %s recoverded" % ysitio)
            elif tipo == 'postgresql_psycopg2':
                cmd = "postgresql... --user=%s --password=%s %s < %s" % (
                    db['USER'], db['PASSWORD'], db['NAME'], origen)
                os.system(cmd)
                mensaje = _("Backup %s recoverded" % origen)
            elif tipo == 'oracle':
                cmd = "oracle... --user=%s --password=%s %s < %s" % (
                    db['USER'], db['PASSWORD'], db['NAME'], origen)
                os.system(cmd)
                mensaje = _("Backup %s recoverded" % origen)
            modeladmin.message_user(request, mensaje, level=messages.SUCCESS) 
    else:
        mensaje = "%s no es un archivo de tipo bakup recuperable" % origen
        modeladmin.message_user(request, mensaje, level=messages.ERROR)                
  
    return

def ac_recuperar_backup(modeladmin, request, queryset):
    for obj in queryset:
        recuperar_backup(modeladmin, request, obj)
    url = ''
    return HttpResponseRedirect(url)
ac_recuperar_backup.short_description = "3. Recuperar base de datos origen"


#------------------------------------
# ELiminar instalacion
#----------------------------------

def borra_database(instal):
	mensaje = "Falta Borrar Base de datos iris_%s" % (instal)
	return mensaje
	#----------------------------------
	# Copia seguridad y Borrar base de datos
	#----------------------------
	fichero = os.path.join(
		settings.RUTA_ACCESO, 'db_borradas', '%s_%s.sql' % (obj.id, obj.alias))
	cmd = "mysqldump --user=%s --password=%s %s > %s" % (
					db['USER'], db['PASSWORD'], db['NAME'], fichero)
	os.system(cmd)
	# Me da problemas si no hago esta espera
	time.sleep(4)
	cmd = "gzip %s" % fichero
	os.system(cmd)
	mensaje = 'Ocupa: %s' % os.stat(fichero).st_size
	modeladmin.message_user(request, mensaje)
	#----------------------------------
	cmd = "mysqladmin --user=%s --password=%s --force drop %s" % (
				db['USER'], db['PASSWORD'], db['NAME'])
	os.system(cmd)
	return mensaje
	

def ac_eliminar_instal(modeladmin, request, queryset):
	
	# - Borrar wsgis
	# - Borrar base de datos
	# - Borrar carpeta media
	
	for obj in queryset:
		#----------------------------------
		# Borrar wsgis
		#----------------------------
		if False:
			ruta_wsgi = os.path.join(
					os.path.dirname(os.path.dirname(settings.BASE_DIR)),
					'espiral', 'multiges', 'multiges', 'wsgis')
			#---------------------
			destino1 = os.path.join(settings.RUTA_ACCESO, "%s.py" % obj.alias)	
			if os.path.isfile(destino1):
				cmd = 'rm %s' % destino1
				mensaje = '%s Ini borrado' % obj.alias
				os.system(cmd)
			else:
				mensaje = 'No existe el fichero .ini %s' % obj.alias
			modeladmin.message_user(request, mensaje)
			#------------------------------
			destino2 = os.path.join(settings.RUTA_ACCESO, "%s.py" % obj.alias)	
			if os.path.isfile(destino2):
				cmd = 'rm %s' % destino2
				mensaje = '%s Ini borrado' % obj.alias
				os.system(cmd)
			else:
				mensaje = 'No existe el fichero .ini %s' % obj.alias
			modeladmin.message_user(request, mensaje)
		#----------------------------------
		# Borrar subcarpeta de zinstal
		#----------------------------
		carpeta_instal = os.path.join(settings.RUTA_ACCESO, obj.alias)
		try:
			os.system("rm -r -f %s" % carpeta_instal)
			mensaje = "Borrada subcarpeta de zinstal %s" % (obj.alias)
		except:
			mensaje = "No existe la subcarpeta %s" % obj.alias
		modeladmin.message_user(request, mensaje)
		#----------------------------------
		# Borrar base de datos
		#----------------------------
		mensaje = borra_database(obj.alias)
		modeladmin.message_user(request, mensaje)
	return
ac_eliminar_instal.short_description = "ELIMINAR INSTALACION"


#---------------------------

	

#-------------------------------


Patron de uso de una base de datos sqlite no definida en el settings

import sqlite3

RUTA_DATOS = os.path.join(settings.BASE_DIR, 'SITES_DATOS', 'qbackupAdmin', 'qbackupAdmin')
db_name = os.path.join(RUTA_DATOS, 'db.sqlite3')

connection = sqlite3.connect(db_name)
cursor = connection.cursor()

consulta = ("SELECT campo1, campo2, .., campon FROM <nombre tabla>")
cursor.execute(consulta)
# cursor devuelve una tabla con una fila por registro y una columna por campo

connection.close()
"""

	

