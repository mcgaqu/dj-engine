# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Line
from PIL import Image

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import iri_to_uri

# from escala.base.actions import accion_atributo
from escala.utils.ficheros import get_carpeta_temp_user
from escala.e1empresa.models import Empresa


def ac_PlanCVpdf(modeladmin, request, queryset):
	#------------------------
	contador = queryset.count()
	docx_alias = queryset[0].alias[:4]

	docx = Docx.objects.get(alias=docx_alias)
	#---------------------
	docx_gen = docx.DocxGenerador(request, docx, queryset)
	docx_gen.render()
	mensaje = "%s: %s pdfs generados" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return HttpResponseRedirect(docx_gen.fichero_url)
ac_PlanCVpdf.short_description = "2.1.- Imprimir en PDF"


def ac_PlanCVxls(modeladmin, request, queryset):
	mensaje = "Pendiente de desarrollo"

	import xlwt
	fichero_dir = get_carpeta_temp(subcarpeta=request.user.username)
	fichero_nombre = "CV_%s_%s.xls" % (info.fecha.strftime('%Y%m%d%H%M%S'), info_id, )

	fichero = os.path.join(fichero_dir, fichero_nombre)

	#------------------------------
	style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
	style1 = xlwt.easyxf('',num_format_str='DD-MMM-YY')
	#------------------------
	wb = xlwt.Workbook() # encoding='iso-8859-1'
	#---------------------
	# Hoja1: Resumen facturación mensual
	#------------------------
	# mes, factura1, facturan, base,
	# base1, cuota1, base2, cuota2, base3, cuota3
	qs = CV.objects.filter(fecha__year=ejercicio)
	#------------------------------
	# Hoja2: Resumen facturación dia
	#-------------------------
	
	#-------------------------
	# 12 Hojas: M01-M12: Registro de Facturas del mes
	#------------------------------

	hoja1 =  "%s_%s.xls" % (info_id, info.fecha.strftime('%Y%m%d%H%M%S'))	
	ws = wb.add_sheet(hoja1, cell_overwrite_ok=True)

	campos_salida = info.get_campos_salida()# [2:]
	cabecera = [x.campo.nombre.capitalize() for x in campos_salida]
	campos_salida = info.get_info_list_display(request)[2:]
	qs = ITDetalle1.objects.all()
	#---------------------
	ws.write(0,0, info.nombre, style0)
	for x, titulo_col in enumerate(cabecera):
		ws.write(1, x, titulo_col)
	y = 1
	for fila in qs:
		y+=1
		for x, campo in enumerate(campos_salida):
			valor = "%s" % getattr(fila, campo) # 'valor'# result_repr(campo)
			ws.write(y, x, valor)
	wb.save(fichero)

	fichero_url = "%stemp/%s/%s" % (
							settings.MEDIA_URL,
							request.user,
							fichero_nombre)
	print(fichero)
	print(fichero_url)
	
	
	return  fichero_url

	modeladmin.message_user(request, mensaje)
	return
ac_PlanCVxls.short_description = "2.2.- Imprimir en XLS"


#====================================

def ac_duplicarCV(modeladmin, request, queryset, pieza=None):

	""" Duplicar CV """
	mensaje = ''
	contador = 0
	for reg in queryset:
		contador +=1
		#----------------------
		# hacer algo
		#----------------------
	mensaje += "%s: %s duplicados" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
	#url = modeladmin.get_urlx(request,1)
	#return HttpResponseRedirect(url)
ac_duplicarCV.short_description = "Entregar Pedido"

def ac_entregarCV(modeladmin, request, queryset, pieza=None):

	""" Entregar Pedido """
	mensaje = ''
	contador = 0
	for reg in queryset:
		contador +=1
		#----------------------
		# hacer algo
		#----------------------
	mensaje += "%s: %s entregados" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
ac_entregarCV.short_description = "Entregar Pedido"

def ac_facturarCV(modeladmin, request, queryset, pieza=None):

	""" Facturar Albaran """
	mensaje = ''
	contador = 0
	for reg in queryset:
		contador +=1
		#----------------------
		# hacer algo
		#----------------------
	mensaje += "%s: %s facturados" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
ac_facturarCV.short_description = "Facturar Albarán"


def ac_contabilizarCV(modeladmin, request, queryset, pieza=None):

	""" Contabilizar Factura """
	mensaje = ''
	contador = 0
	for reg in queryset:
		contador +=1
		#----------------------
		# hacer algo
		#----------------------
	mensaje += "%s: %s contabilizadas" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
ac_contabilizarCV.short_description = "Contabilizar Factura"


def ac_pagarCV(modeladmin, request, queryset, pieza=None):
	""" Pagar Factura """
	mensaje = ''
	contador = 0
	for reg in queryset:
		contador +=1
	mensaje += "%s: %s pagadas" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
ac_pagarCV.short_description = "Pagar CV"


def genera_plantilla_pdfCV(modeladmin, request):
	#--------------------------
	# Defino el diseño de la página común a todos los documentos
	#-------------------------
	ALTO_PAGINA=29.7*cm
	ANCHO_PAGINA=21*cm
	#---------------
	# Fuentes
	#-----------------
	ruta_base = os.path.join(settings.BASE_DIR, 'escala/admin1/static', 'theme')
	ruta_fuentes = os.path.join(ruta_base, 'fonts')
	font1 = os.path.join(ruta_fuentes, "arial.ttf")
	font2 = os.path.join(ruta_fuentes, "arialbd.ttf")
	font3 = os.path.join(ruta_fuentes, "arialbi.ttf")
	font4 = os.path.join(ruta_fuentes, "ariali.ttf")
	#importar una fuente TT
	pdfmetrics.registerFont(TTFont('DejaVu', font1)) # 'DejaVuSans.ttf'))
	pdfmetrics.registerFont(TTFont('DejaVuBd', font2)) # 'DejaVuSansBold.ttf'))
	pdfmetrics.registerFont(TTFont('DejaVuBdIt', font3)) # 'DejaVuSansBoldOblique.ttf'))
	pdfmetrics.registerFont(TTFont('DejaVuIt',font4)) # 'DejaVuSansOblique.ttf'))
	registerFontFamily('Dejavu', normal = 'DejaVu', bold = 'DejaVuBd', italic = 'DejaVuIt', boldItalic = 'DejaVuBdIt')
	#-------------------------
	# Lineas
	#-----------------------
	l1 = (1*cm, ALTO_PAGINA-2.3*cm, ANCHO_PAGINA-1.5*cm, ALTO_PAGINA-2.3*cm)
	l2 = (1*cm, 2.0*cm, ANCHO_PAGINA-1.5*cm, 2.0*cm)
	lineas = [l1,l2]	
	#-------------------------	
	# Estilos
	#----------------------------
	estiloencabezado = ParagraphStyle('',
								  fontName = 'DejaVuBd',
								  fontSize = 10,
								  alignment = 0,
								  spaceBefore = 0,
								  spaceAfter = 0,
								  leftIndent = -1*cm,
								  rightIndent = -0.7*cm)
	
	estilonormal = ParagraphStyle('',
								  fontName = 'DejaVu',
								  fontSize = 10,
								  alignment = 4,
								  spaceBefore = 0,
								  spaceAfter = 0,
								  firstLineIndent = 1*cm,
								  topIndent =-1*cm,
								  leftIndent = -1*cm,
								  rightIndent = -0.7*cm)
	estilo1 = ParagraphStyle('',
								  fontName = 'DejaVu',
								  fontSize = 10,
								  alignment = 4,
								  spaceBefore = 0,
								  spaceAfter = 0,
								  firstLineIndent = 1*cm,
								  topIndent =-1*cm,
								  leftIndent = 10*cm,
								  rightIndent = -0.7*cm)
	#--------------------------
	# Defino las variables de datos común a todos los documentos
	#-------------------------
	# ruta_base = os.path.join(settings.BASE_DIR, 'escala/admin1/static', 'theme')
	ruta_logo = os.path.join(ruta_base, 'img', 'sicem_logo.png')
	logo = Image.open(ruta_logo)
	emp_calle = 'C/Loja, Parcela 7, Local 13'
	emp_poblacion = '18220 Albolote (Granada)'
	emp_tel = 'Tel: 958 888 291'
	pie1 = 'Software Integrado para el Control de Empresa, S.L. C.I.F.: B-18.521.971'
	pie2 = 'Inscripción en el Registro Mercantil:'
	pie2 += ' TOMO:874, LIBRO:0, FOLIO:131, SECCION:8, HOJA:GR-15574, INSCRIP:1'
	#-------------------------------------------
	# Pages
	#--------------------------- 
	def myFirstPage(canvas, doc):

		canvas.saveState()
		#-----------------------------    Lineas
		canvas.setStrokeColor('Grey')
		canvas.setLineWidth(0.01)
		canvas.lines(lineas)
		#-----------------------------   Textos
		canvas.setFont('DejaVu',7)
		#----------------------------
		# Cabecera
		#------------------------------------
		canvas.drawInlineImage(logo, 1*cm, ALTO_PAGINA-2.*cm, width = 150, height = 50)
		canvas.drawRightString(ANCHO_PAGINA-1.7*cm, ALTO_PAGINA-1*cm, emp_calle)
		canvas.drawRightString(ANCHO_PAGINA-1.7*cm, ALTO_PAGINA-1.5*cm, emp_poblacion)
		canvas.drawRightString(ANCHO_PAGINA-1.7*cm, ALTO_PAGINA-2.*cm, emp_tel)
		#----------------------------
		# Pie
		#------------------------------------
		canvas.drawCentredString(ANCHO_PAGINA/2.0, 1.5 * cm, u'%s' % pie1)
		canvas.drawCentredString(ANCHO_PAGINA/2.0, 1.0 * cm, u'%s' % pie2)		
		canvas.drawRightString(ANCHO_PAGINA - 1.7 * cm, 1.5 * cm, u'Pág. %d' % doc.page)

		canvas.restoreState()
	
	def myLaterPages(canvas, doc):
		canvas.saveState()
		#-----------------------------    Lineas
		canvas.setStrokeColor('Grey')
		canvas.setLineWidth(0.01)
		canvas.lines(lineas)
		#-----------------------------   Textos
		canvas.setFont('DejaVu',7)
		#----------------------------
		# Cabecera
		#------------------------------------
		canvas.drawInlineImage(logo, 1*cm, ALTO_PAGINA-2.*cm, width = 150, height = 50)
		canvas.drawRightString(ANCHO_PAGINA-1.7*cm, ALTO_PAGINA-1*cm, emp_calle)
		canvas.drawRightString(ANCHO_PAGINA-1.7*cm, ALTO_PAGINA-1.5*cm, emp_poblacion)
		canvas.drawRightString(ANCHO_PAGINA-1.7*cm, ALTO_PAGINA-2.*cm, emp_tel)
		#----------------------------
		# Pie
		#------------------------------------
		canvas.drawCentredString(ANCHO_PAGINA/2.0, 1.5 * cm, u'%s' % pie1)
		canvas.drawCentredString(ANCHO_PAGINA/2.0, 1.0 * cm, u'%s' % pie2)		
		canvas.drawRightString(ANCHO_PAGINA - 1.7 * cm, 1.5 * cm, u'Pág. %d' % doc.page)
	#------------------------------
	# funcion generacion del documento
	#-----------------------------------
	def get_Story(datos):
		Story = [Spacer(1,cm)]
		#--------------------------
		Story.append(Paragraph(datos['obj'].tercero.nombre, estilo1))
		Story.append(Paragraph(datos['obj'].tercero.att, estilo1))
		Story.append(Paragraph(datos['obj'].tercero.calle, estilo1))
		Story.append(Paragraph(datos['obj'].tercero.poblacion.nombre, estilo1))
		#------------------------------------------
		Story.append(Paragraph("FACTURA Nº: %s" % datos['obj'].alias, estiloencabezado))
		Story.append(Paragraph("Fecha: %s" % datos['obj'].fecha, estiloencabezado))
		Story.append(Paragraph("Código Cliente: %s" % datos['obj'].tercero.alias, estiloencabezado))
		Story.append(Paragraph("N.I.F. Cliente: %s" % datos['obj'].tercero.nif, estiloencabezado))
		Story.append(Spacer(1,2*cm))
		#-------------------------------
		# Cuerpo de la factura
		#-----------------------------------
		filas = [[
			# 'Producto',
			('%s' % 'Descripción').ljust(30, ' '),
			('%s' % 'Unidades').rjust(10, ' '),
			('%s' % 'Precio').rjust(10, ' '),
			('%s' % 'Importe').rjust(12, ' ')
			 ]]
		for lin in datos['obj'].LR_lineas_producto:
			filas.append([
				# "%s" % lin.producto.alias,
				"%s %s%s" % (lin.producto.nombre, lin.nombre, lin.notas),
				"%s" % lin.unidades,
				"%s" % lin.precio,
				"%s" % lin.importe_base
			])
		tabla = Table(filas)
		#tabla.setStyle([
		#	('TEXTCOLOR',(0,0),(-1,0),colors.red),
		#	('TEXTCOLOR',(0,1),(-1,-1),colors.blue)
		#	])
		# tabla.setStyle([('BACKGROUND',(0,0),(-1,0),colors.grey)])
		tabla.setStyle([('BOX',(0,0),(-1,-1),0.25, colors.green)])
		tabla.setStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.grey)])
		Story.append(tabla)
		Story.append(Spacer(1,2*cm))
		#---------------------------------------
		# Tottales
		#--------------------------
		Story.append(Paragraph("%sBase Imponible: %s" % (
			' '*20, datos['obj'].total_base), estilo1))
		Story.append(Paragraph("%sI.V.A: (21):    %s" % (
			' '*20, (datos['obj'].total_facturar-datos['obj'].total_base)), estilo1))
		Story.append(Paragraph("%sTotal Factura:  %s" % (
			' '*20, datos['obj'].total_facturar), estilo1))
		return Story

	def x_get_Story(datos):
		Story = []
		for x in range(2):
			Story.append(Spacer(1,cm))
			#--------------------------
			Story.append(Paragraph(datos['obj'].tercero.nombre, estilo1))
			Story.append(Paragraph(datos['obj'].tercero.att, estilo1))
			Story.append(Paragraph(datos['obj'].tercero.calle, estilo1))
			Story.append(Paragraph(datos['obj'].tercero.poblacion.nombre, estilo1))
			#------------------------------------------
			Story.append(Paragraph("FACTURA Nº: %s" % datos['obj'].alias, estiloencabezado))
			Story.append(Paragraph("Fecha: %s" % datos['obj'].fecha, estiloencabezado))
			Story.append(Paragraph("Código Cliente: %s" % datos['obj'].tercero.alias, estiloencabezado))
			Story.append(Paragraph("N.I.F. Cliente: %s" % datos['obj'].tercero.nif, estiloencabezado))
			Story.append(Spacer(1,2*cm))
			#-------------------------------
			# Cuerpo de la factura
			#-----------------------------------
			filas = [[
				# 'Producto',
				('%s' % 'Descripción').ljust(30, ' '),
				('%s' % 'Unidades').rjust(10, ' '),
				('%s' % 'Precio').rjust(10, ' '),
				('%s' % 'Importe').rjust(12, ' ')
				 ]]
			for lin in datos['obj'].LR_lineas_producto:
				filas.append([
					# "%s" % lin.producto.alias,
					"%s %s%s" % (lin.producto.nombre, lin.nombre, lin.notas),
					"%s" % lin.unidades,
					"%s" % lin.precio,
					"%s" % lin.importe_base
				])
			tabla = Table(filas)
			#tabla.setStyle([
			#	('TEXTCOLOR',(0,0),(-1,0),colors.red),
			#	('TEXTCOLOR',(0,1),(-1,-1),colors.blue)
			#	])
			# tabla.setStyle([('BACKGROUND',(0,0),(-1,0),colors.grey)])
			tabla.setStyle([('BOX',(0,0),(-1,-1),0.25, colors.green)])
			tabla.setStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.grey)])
			Story.append(tabla)
			Story.append(Spacer(1,2*cm))
			#---------------------------------------
			# Tottales
			#--------------------------
			Story.append(Paragraph("%sBase Imponible: %s" % (
				' '*20, datos['obj'].total_base), estilo1))
			Story.append(Paragraph("%sI.V.A: (21):    %s" % (
				' '*20, (datos['obj'].total_facturar-datos['obj'].total_base)), estilo1))
			Story.append(Paragraph("%sTotal Factura:  %s" % (
				' '*20, datos['obj'].total_facturar), estilo1))
			
			Story.append(Spacer(1,13*cm))
		return Story
	#-----------------------
	def get_fichero_nombre(obj_id):
		return os.path.join(get_carpeta_temp_user(request.user.username), '%s_%s.pdf' % (
			modeladmin.model.__name__, obj_id))
	#--------------------------------
	return (get_fichero_nombre, x_get_Story, myFirstPage, myLaterPages)


def genera_pdfCV(tipo, obj, get_fichero_nombre, get_Story, myFirstPage, myLaterPages):
	#------------------------
	# Defino las variables de datos de cada documento
	#----------------------
	datos = dict(
		obj = obj,
	)
	fichero_nombre = get_fichero_nombre(obj.id)
	#-------------------------	
	# Genero el documento
	#----------------------------
	if not tipo in (1,2,3):
		tipo = 2
	if tipo == 1:
		#---------------------
		# crea-salva
		#----------------------------
		doc = SimpleDocTemplate(fichero_nombre)
		doc.build(get_Story(datos), onFirstPage=myFirstPage, onLaterPages=myLaterPages)
		return fichero_nombre			

	elif tipo == 2:
		#---------------------
		# crea-salva y descarga
		#----------------------------
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="%s"' %  fichero_nombre
		doc = SimpleDocTemplate(response)
		doc.build(get_Story(datos), onFirstPage=myFirstPage, onLaterPages=myLaterPages)
		return response

	else:
		#---------------------
		# crea-salva, descarga y levanta
		#----------------------------
		doc = SimpleDocTemplate(fichero_nombre)
		doc.build(get_Story(datos), onFirstPage=myFirstPage, onLaterPages=myLaterPages)
		fichero_url = "%s%s/%s/%s_%s.pdf" % (
								settings.STATIC_URL,
								settings.INSTAL,
								request.user,
								modeladmin.model.__name__,
								obj.id)
		return  HttpResponseRedirect(fichero_url)	
	

def ac_pdfCV(modeladmin, request, queryset, pieza=None):

	mensaje = ''
	contador = 0
	get_fichero_nombre, get_Story, myFirstPage, myLaterPages = 	genera_plantilla_pdfCV(
		modeladmin, request)
	for obj in queryset:
		contador +=1
		return genera_pdfCV(2, obj, get_fichero_nombre, get_Story, myFirstPage, myLaterPages)
	mensaje += "%s: %s pdfs generados" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
ac_pdfCV.short_description = "Generar pdf de CV"


def ac_email_pdfCV(modeladmin, request, queryset, pieza=None):

	""" Enviar email """
	
	from django.core.mail import EmailMessage, get_connection
	
	mensaje = ''
	contador = 0
	correos = []
	get_fichero_nombre, get_Story, myFirstPage, myLaterPages = genera_plantilla_pdfCV(
													modeladmin, request)

	for reg in queryset:
		contador +=1
		#----------------------
		correo = (EmailMessage(
			'Mensaje para %s' % reg.nombre,
			'Here is the message.',
			'mc@multiges.net',
			[reg.email]			
		))
		#--------------------
		fichero_nombre = genera_pdfCV(obj, get_fichero_nombre, get_Story, myFirstPage, myLaterPages)
		correo.attach_file(fichero_nombre)
		correos.append(correo)
		#--------------------------
	if contador:
		connection = get_connection()   # Use default email connection
		connection.send_messages(correos)
		#----------------------
	mensaje += "%s: %s emails enviados" % (contador, modeladmin.model.__name__)
	modeladmin.message_user(request, mensaje)
	return
ac_email_pdfCV.short_description = "Enviar pdf de CV por Email"


def ac_txtCV(modeladmin, request, queryset, pieza=None):
	emp = Empresa.objects.get(alias=settings.INSTAL)
	filas_emp = [
		"%s" % (emp.nombre),
		"%s" % (emp.calle),
		"%s" % (emp.poblacion),
		"Teléfono: %s" % (emp.tel),
		"C.I.F: %s" % (emp.nif),
		# "P.V.P. IVA INCLUIDO"
	]
	filas = []
	for obj in queryset:
		filas += filas_emp
		filas.append('%s  %s' % (obj.fecha1, obj.hora1))
		filas.append('Num: %s' % (obj.alias))
		for cvp in obj.cvproducto_set.all():
			filas.append("%s %s %s %s" % (
				cvp.unidades, cvp.producto.nombre, cvp.precio, cvp.importe_base))
		filas.append("TOTAL %s EUROS" % obj.total_base)
		filas.append("IVA BASE IMPONIBLE CUOTA")
		for cvt in obj.cvtasa_set.all():
			filas.append("%s %s %s" % (
				cvt.tasa.porc,
				cvt.importe_base,
				cvt.importe_iva
			))
		filas.append('')
		filas.append('')
		
	#-----------------------
	# Escribir fichero
	#---------------------------
	fichero = os.path.join(
		get_carpeta_temp_user(request.user.username), 'tickets_%s.txt' % emp.alias)
	f = open(fichero, 'w')
	texto = ''
	for fila in filas:
		texto += '%s\n' % fila
	f.write(texto.encode('iso-8859-1'))
	f.close()

	#------------------
	fichero_url = "%s%s/%s/tickets_%s.txt" % (
							settings.STATIC_URL,
							settings.INSTAL,
							request.user,
							emp.alias)
	return  HttpResponseRedirect(fichero_url)
ac_txtCV.short_description = "Generar tickets en txt para imprimir"