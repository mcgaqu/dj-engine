# -*- coding: utf-8 -*-
from django.contrib import messages

import os
import xlwt

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
# from django.utils import six
from django.utils.encoding import iri_to_uri

from mod_admin.utils.base import print_msg
from mod_admin.utils.ficheros import get_carpeta_media, get_carpeta_temp
from mod_admin.utils.ficheros import get_carpeta_temp_user
# from escala.c7docxs.models import Docx

from mod_auth.companies.models import Company

from mod_make.plans.models import Plan, PlanCV, PlanCVTax
from mod_make.plans.adminextra import PlanCVAdmin1Extra, PlanAdmin1Extra



def informe_periodo(modeladmin, request, obj, carpeta_path, pdf=False):
    #---------------------
    # borrar y crear la carpeta de informes del periodo
    #-----------------------------
    try:
        os.system("rm -r -f %s" % carpeta_path)
    except:
        # import pdb; pdb.set_trace()
        pass
    os.mkdir(carpeta_path) # informes
    nombre = obj.alias
    carpeta1_path = os.path.join(carpeta_path, nombre)
    os.mkdir(carpeta1_path)
    #-----------------------------
    # Informe excel con 14 hojas: <obj.alias>.xls
    #---------------------------------
    fichero_path = os.path.join(carpeta1_path, "%s.xls" % nombre)
    style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
    style_fecha = xlwt.easyxf('',num_format_str='DD-MMM-YY')
    style_decimal = xlwt.easyxf('align: horiz right', num_format_str='#,##0.00')
    style_entero = xlwt.easyxf('align: horiz right', num_format_str='#,##0')
    wb = xlwt.Workbook() # encoding='iso-8859-1'
    # td_cv = obj.doctype
    #------------------------------------
    # titulo = "Informes del Periodo %s" % obj.alias

    def escribe_informe(ws, y0, x0, qs, titulo, cabecera, campos):
        ws.write(y0, x0, titulo, style0)
        for x, titulo_col in enumerate(cabecera):
            ws.write(y0+1, x0+x, titulo_col)
            y = y0+1
            for fila in qs:
                y+=1
                valor = ''
                for x, campo in enumerate(campos):
                    if hasattr(fila, campo):
                        valor = getattr(fila, campo) # 'valor'# result_repr(campo)
                        # valor = result_repr(fila, campo, modeladmin)
                    else:
                        extra_cv = PlanAdmin1Extra()
                        if hasattr(extra_cv, campo):
                            valor = getattr(extra_cv, campo)(fila)
                    #if campo == 'importe_base':
                    #	import pdb; pdb.set_trace()
                    if type(valor).__name__ in ('int', 'long'):
                        ws.write(y, x0+x, valor, style_entero)
                    elif type(valor).__name__ in ('Decimal', 'float'):
                        ws.write(y, x0+x, valor, style_decimal)
                    elif type(valor).__name__ in ('date',):
                        ws.write(y, x0+x, "%s" % valor, style_fecha)
                    else:
                        ws.write(y, x0+x, "%s" % valor)
                    #if campo in (
                    #	'total_facturar', 'CD_sum_total_facturar',
                    #			'total_base', 'CD_total_cuota', 'total_facturar',
                    #			'importe_base', 'importe_iva'):
                    #	ws.write(y, x0+x, valor, style2)
                    #else:
                    #	ws.write(y, x0+x, "%s" % valor)
        return
    #--------------------
    # Ventas mes - dia
    #------------------------
    ws = wb.add_sheet("%s_VENTAS" % obj.alias, cell_overwrite_ok=True)
    #--------------------------------
    titulo = "VENTAS MES del Periodo %s" % obj.alias
    cabecera = ('Mes', 'Nº Facturas Emitidas', 'Base Imponible', 'Cuota IVA',
                'Total Facturas', 'Fra.Inicial:Final')
    # campos = ('alias', 'num_int', 'ED_amount_base', 'ED_amount_tax',
    #             'ED_amount_total', 'EC_cvs_ini_fin_sort')
    campos = ('alias', 'num_int', 'num_dec1', 'ED_tax1', 'ED_total1',
                'EC_cvs_ini_fin_sort')
    qs = Plan.objects.filter(
            alias__startswith=obj.alias, level=2).order_by('alias')
    num_meses = qs.count()

    escribe_informe(ws, 0, 0, qs, titulo, cabecera, campos)
    #------------------------
    titulo = "VENTAS DIA del Periodo %s" % obj.alias
    cabecera = ('Fecha', 'Día Semana', 'Nº Facturas Emitidas', 
                    'Total Facturas',  'Fra.Inicial:Final')
    # campos = ('MC_date1', 'MC_date1_diasem', 'num_int',
    #             'ED_amount_total', 'EC_cvs_ini_fin_sort')
    campos = ('MC_date', 'MC_date_diasem', 'num_int',
                'ED_total1', 'EC_cvs_ini_fin_sort')
    qs = Plan.objects.filter(
            alias__startswith=obj.alias, level=3).order_by('alias')
    escribe_informe(ws, num_meses+5, 0, qs, titulo, cabecera, campos)
    #---------------------
    # Registros por meses
    #---------------------
    if False:
        meses = PlanCV.objects.filter(alias__startswith=obj.alias, nivel=2)
        for mes in meses:
            ws = wb.add_sheet(mes.alias, cell_overwrite_ok=True)
            #---------------------------------
            titulo = "FACTURAS del mes %s" % mes.alias
            cabecera = ( 'Fecha', 'Número','Base Imponible', 'Cuota IVA', 'Total Factura')
            campos = ('MC_date1', 'sort',  'amount_base', 'amount_tax', 'amount_total')
            qs = PlanCV.objects.filter(
                    alias__startswith=mes.alias, internal=False).order_by('alias')
            escribe_informe(ws, 0, 0, qs, titulo, cabecera, campos)
            #--------------------
            titulo = "REGISTROS DE IVA del Periodo %s" % obj.alias
            cabecera = ('Fecha', 'Número', 'Base Imponible', 'Tipo IVA', 'Cuota IVA')
            campos = ('MC_date1', 'sort', 'amount_base', 'porc_tax', 'amount_tax')
            qs = PlanCVTax.objects.filter(
                    cv__alias__startswith=mes.alias, cv__internal=False).order_by('cv__alias')
            escribe_informe(ws, 0, 6, qs, titulo, cabecera, campos)

    wb.save(fichero_path)		
    
    #---------------------------------
    # un fichero pdf por cada dia con las facturas del día
    #------------------------------
    # import pdb; pdb.set_trace()
    if pdf:
        #---------------------------------
        # TODO !!! un fichero pdf por cada dia con las facturas del día
        #------------------------------
        # from escala.c7docxs.models import Docx
        # for mes in meses:
        #     carpeta2_path = os.path.join(carpeta1_path, mes.alias)
        #     os.mkdir(carpeta2_path)
        #     dias = Plan.objects.filter(alias__startswith=mes.alias, nivel=3)
        #     #----------------------------
        #     print_msg("%s %s" % (mes.alias, dias.count()))
        #     for dia in dias:
        #         cvs = PlanCV.objects.filter(alias__startswith=dia.alias, interno=False)
        #         if cvs:
        #             # import pdb; pdb.set_trace()
        #             fichero = os.path.join(carpeta2_path, "%s.pdf" % dia.alias)
        #             docx = Docx.objects.get(alias=td_cv.alias)
        #             docx.DocxGenerador(request, docx, cvs).render(fichero=fichero) 
        print_msg("Se ha creado el informe pdf para el periodo %s" % obj.alias)
    else:
        print_msg("Se ha creado el informe xls del periodo %s" % obj.alias)
    return 


def ac_export_planreport_pdf(modeladmin, request, queryset):
	#-----------------------
	if queryset.count() > 1:
		mensaje = "Sólo puede seleccionar un periodo para obtener informes"
		modeladmin.message_user(request, mensaje)
		return
	carpeta_user_path, carpeta_user_url = get_carpeta_temp_user(request.user.username)
	carpeta_nombre = 'informes'
	carpeta_path = os.path.join(carpeta_user_path, carpeta_nombre)
	obj = queryset[0]


	informe_periodo(modeladmin, request, obj, carpeta_path, pdf=True)
	#-----------------
	# enzipar carpeta y devolverla
	#-----------------------------
	fichero_nombre = '%s.zip' % carpeta_nombre
	fichero_path = os.path.join(os.path.dirname(carpeta_path), fichero_nombre)
	try:
		os.remove(fichero_path)
	except:
		pass
	#------------------------
	cmd1 = "zip -r %s %s/" % (fichero_path, carpeta_path)
	#--------------------
	os.system(cmd1)
	#-------------------------------
	fichero_url = "%s/%s" % (carpeta_user_url, fichero_nombre)
	mensaje = "Se ha creado el informe pdf para el periodo %s" % obj.alias	
	modeladmin.message_user(request, mensaje)
	return HttpResponseRedirect(fichero_url)
ac_export_planreport_pdf.short_description = "INFORMES de Periodos en Pdf"


def ac_export_planreport_xls(modeladmin, request, queryset):
	#-----------------------
	if queryset.count() > 1:
		mensaje = "Sólo puede seleccionar un periodo para obtener informes"
		modeladmin.message_user(request, mensaje)
		return
	carpeta_user_path, carpeta_user_url = get_carpeta_temp_user(request.user.username)
	carpeta_nombre = 'informes'
	carpeta_path = os.path.join(carpeta_user_path, carpeta_nombre)
	obj = queryset[0]


	informe_periodo(modeladmin, request, obj, carpeta_path, pdf=False)
	#-----------------
	# enzipar carpeta y devolverla
	#-----------------------------
	fichero_nombre = '%s.zip' % carpeta_nombre
	fichero_path = os.path.join(os.path.dirname(carpeta_path), fichero_nombre)
	try:
		os.remove(fichero_path)
	except:
		pass
	#------------------------
	cmd1 = "zip -r %s %s/" % (fichero_path, carpeta_path)
	#--------------------
	os.system(cmd1)
	#-------------------------------
	fichero_url = "%s/%s" % (carpeta_user_url, fichero_nombre)
	mensaje = "Se ha creado el informe excel para el periodo %s" % obj.alias	
	modeladmin.message_user(request, mensaje)
	return HttpResponseRedirect(fichero_url)
ac_export_planreport_xls.short_description = "INFORMES de Periodos en excel"

