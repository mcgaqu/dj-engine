# -*- coding: utf-8 -*-



import os, time, datetime, decimal, random, calendar
from typing import Counter
from django.db.models.aggregates import Count
import xlrd, xlwt
from django.conf import settings
from django.contrib import messages

from django.db.models import Sum
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
from django.template.response import TemplateResponse
# from django.utils.html import format_html

# from escala.base.actions import accion_atributo
# from escala.e2tipodocs.models import TipoDoc, get_crear_tipodoc

from mod_admin.utils.base import print_msg, get_dates_from_period
from mod_auth.companies.models import Company
from mod_auth.doctypes.models import DocType, get_create_doctype
from mod_entity.products.models import Product
from mod_entity.projects.models import Project, ProjectAux
from mod_make.plans.models import Plan


#----------------------------
# Company
#-------------------------------

def ac_create_projects(modeladmin, request, queryset, pieza=None):
    if queryset.count() > 1:
        mensaje = "Este proceso sólo se puede realizar para un registro"
        modeladmin.message_user(request, mensaje, messages.WARNING)
        return
    #-----------------------
    obj = queryset[0]
    if obj.locked: # or plan.level != 1:
        mensaje = "Registro %s bloqueado o nivel != 1. \n" % obj.alias
        modeladmin.message_user(request, mensaje, messages.WARNING)
        return
    if not obj.file:
        mensaje = "No se ha definido fichero de datos"
        modeladmin.message_user(request, mensaje, messages.WARNING)
        return
    #-----------------------
    count = 0
    company = obj
    file_path = company.file.path
    wb = xlrd.open_workbook(file_path)
    #----------------------
    if not wb.sheets():
        mensaje = "No se han definido proyectos"
        modeladmin.message_user(request, mensaje, messages.WARNING)
        return
    #--------------------
    dt = get_create_doctype(company, 'Project')
    for s in wb.sheets():
        # TODO!!! comprobar que el nombre de la hoja es un entero entre 2015 y 2030
        if s.name < "2000" or s.name > "2050":
            continue
        count +=1
        try:
            project = Project.objects.get(doctype=dt, alias=s.name)
            mensaje = "El Ejercicio %s ya existe." %  s.name
            modeladmin.message_user(request,mensaje, messages.WARNING)
        except Project.DoesNotExist:
            project = Project(doctype=dt, alias=s.name)
            project.name = s.name
            project.save()
            mensaje = "Ejercicio %s creado." %  s.name
            modeladmin.message_user(request,mensaje, messages.SUCCESS)
    mensaje = "Se han creado %s projectos" % count
    modeladmin.message_user(request, mensaje, messages.SUCCESS)
    return
ac_create_projects.short_description = "Crear Projects/Company"

#----------------------------
# Project
#-------------------------------

def ac_import_planyear(modeladmin, request, queryset, pieza=None):
    count = 0
    for project in queryset:
        if not project.doctype.company.file:
            mensaje = "No se ha definido fichero de datos en la empresa"
            modeladmin.message_user(request, mensaje, messages.WARNING)
            continue
        if project.locked:
            mensaje = "Project %s bloqueado" % project.alias
            modeladmin.message_user(request, mensaje, messages.WARNING)
            continue
        count +=1
        anyo = project.alias  
        fichero = project.doctype.company.file.path
        book = xlrd.open_workbook(fichero)
        sh = book.sheet_by_name(project.alias)
        mensaje = import_tarifa(sh, project)
        modeladmin.message_user(request, mensaje, messages.SUCCESS)
        mensaje = import_peso(sh, project)
        modeladmin.message_user(request, mensaje, messages.SUCCESS)
        mensaje = import_sales(sh, project)
        modeladmin.message_user(request, mensaje, messages.SUCCESS)
        # mensaje = import_pays(sh, project)
        # modeladmin.message_user(request, mensaje, messages.SUCCESS)
    mensaje = "Se han importado %s projectos" % count
    modeladmin.message_user(request, mensaje, messages.SUCCESS)
    return
ac_import_planyear.short_description = "1.- Importar Plan/Año"

#--------------------------
# IMPORTAR FICHERO: 
#-----------------------------------

def import_tarifa(sh, project):
    year = int(project.alias)
    dt = get_create_doctype(project.doctype.company, 'Product')
    count1 = 0
    for rx in range(2, sh.nrows):
        datos = sh.row(rx)[0:7]
        if not datos[0].value:
            break
        count1 +=1
        alias = "%03d" % int(datos[0].value)
        
        #-------------------------------
        try:
            t = ProjectAux.objects.get(trunk=project, inline='TARIFA', alias=alias)
        except ProjectAux.DoesNotExist:
            t = ProjectAux(trunk=project, inline='TARIFA',  alias=alias)   
        t.name = datos[1].value.strip().upper()
        t.num_dec = decimal.Decimal(datos[2].value) # precio
        t.num_int = int(datos[3].value) # peso
        t.grade = datos[4].value.strip() # grupo B=asico, C=omplementario
        t.mark = "%s" % datos[5].value # tipo iva 
        if datos[6].value:
            t.num_int1 = int(datos[6].value) #  variacion
        t.save()
        #------
        try:
            p = Product.objects.get(doctype=dt, alias=alias)
        except Product.DoesNotExist:
            p = Product(doctype=dt, alias=alias)
        p.name = datos[1].value.strip().upper()
        p.save()
    return "%s: %s Tarifas cargadas" % (year, count1)     


def get_prioridad(fv):
    if fv.fecha1 != None and not fv.fecha2 and not fv.marca:
        return 0
    if fv.fecha1 != None and fv.fecha2 != None:
        if not fv.marca:
            return 2
        else:
            return 1
    return 3

def import_peso(sh, project):
    year = int(project.alias)
    #------------------
    # 1 Importar dias semana
    #-------------------------
    count =0
    for rx in range(2, 9):
        count +=1
        datos = sh.row(rx)[9:11]
        celda = "%03d_%03d" % (rx, 9)
        alias = "DIASEM_%s" % (rx-1) # , datos[0].value.strip().upper())
        #-------------------------------
        try:
            f = ProjectAux.objects.get(trunk=project, inline='PESO', alias=alias)
        except ProjectAux.DoesNotExist:
            f = ProjectAux(trunk=project, inline='PESO',  alias=alias)   
        f.name = datos[0].value.strip()
        f.num_int = 0 if not datos[1].value else int(datos[1].value)
        # f.grade = 'DIASEM' 
        # f.sort = "DIASEM_%03d" % rx
        # f.num_int1 = get_prioridad(f)
        f.save()   

    #-----------------------
    # 2 Importar meses
    #-----------------------
    count =0
    for rx in range(2, 14):
        count +=1
        datos = sh.row(rx)[7:9]
        celda = "%03d_%03d" % (rx, 7)
        alias = "M%02d" % (rx-1)
        #-------------------------------
        try:
            f = ProjectAux.objects.get(trunk=project, inline='PESO', alias=alias)
        except ProjectAux.DoesNotExist:
            f = ProjectAux(trunk=project, inline='PESO',  alias=alias)   
        f.name = datos[0].value.strip().upper()
        f.num_int = 0 if not datos[1].value else int(datos[1].value)
        # f.grade = 'MES' 
        # f.sort = "MES_%03d" % rx
        # f.num_int1 = get_prioridad(f)
        f.save()   
    #------------------------
    # 3 Importar dias especiales
    #-----------------------------
    for rx in range(17, sh.nrows):
        datos = sh.row(rx)[7:11]
        if not datos[0].value:
            break
        count +=1
        celda = "%03d_%03d" % (rx, 7)
        alias = "FIESTA_%02d_%s" % (rx-16, datos[0].value.strip().upper())
        #-------------------------------
        try:
            f = ProjectAux.objects.get(trunk=project, inline='PESO', alias=alias)
        except ProjectAux.DoesNotExist:
            f = ProjectAux(trunk=project, inline='PESO',  alias=alias)   
        f.name = datos[0].value.strip().upper()
        f.num_int = 0 if not datos[1].value else int(datos[1].value)
        # f.grade = 'FIESTA' 
        # f.sort = "FIESTA_%03d" % rx
        # f.num_int1 = get_prioridad(f)
        if datos[2].value:
            f1 = xlrd.xldate_as_tuple(datos[2].value, 0)
            f.date1 = datetime.date(f1[0], f1[1], f1[2])
        if datos[3].value:
            f2 = xlrd.xldate_as_tuple(datos[3].value, 0)
            f.date2 = datetime.date(f2[0], f2[1], f2[2])
        f.save()    
    return "%s: %s Factores cargados" % (year, count)

def import_sales(sh, project):
    year = int(project.alias)
    niveles = {'A':0, 'T':1, 'M':2, 'D':3}
    count = 0
    for rx in range(2, sh.nrows):
        datos = sh.row(rx)[12:21]
        if not datos[0].value:
            break        
        celda = "%03d_%03d" % (rx, 12)
        periodo = datos[1].value.strip().upper()
        if periodo == "T":
            alias = "%sT%s" % (year, datos[2].value)
        elif periodo == 'M':
            trimestre = int((datos[2].value-1)/3 + 1 )
            alias = "%sT%sM%02d" % (year, trimestre, int(datos[2].value))
        else:
            alias = celda
        count +=1
        #-------------------------------
        try:
            f = ProjectAux.objects.get(trunk=project, inline='VENTA', alias=alias)
        except ProjectAux.DoesNotExist:
            f = ProjectAux(trunk=project, inline='VENTA',  alias=alias)   
        # f.name = "%s_%s_%s" % (datos[1].value.strip().upper(), datos[2].value, datos[3].value)
        f.num_int = 0 if not datos[4].value else int(datos[4].value) # Nº facturas
        f.num_int1 = 0 if not datos[5].value else int(datos[5].value)
        f.num_dec1 = decimal.Decimal((datos[6].value))
        f.num_int2 = 0 if not datos[7].value else int(datos[7].value)
        f.num_dec2 = decimal.Decimal((datos[8].value))
        f.save()        
    return "%s: %s Ventas cargadas" % (year, count)


def import_pays(sh, project):
    year = int(project.alias)
    count = 0
    for rx in range(2, sh.nrows):
        datos = sh.row(rx)[22:25]
        if not datos[0].value:
            break        
        celda = "%03d_%03d" % (rx, 22)
        count +=1
        f1 = xlrd.xldate_as_tuple(datos[0].value, 0)
        fecha1 = datetime.date(f1[0], f1[1], f1[2])    
        #-------------------------------
        try:
            f = ProjectAux.objects.get(trunk=project, inline='PAGO', alias=celda)
        except ProjectAux.DoesNotExist:
            f = ProjectAux(trunk=project, inline='PAGO',  alias=celda)  
        f.date1 = fecha1 
        f.name = f.alias
        f.num_dec = decimal.Decimal((datos[6].value)) # Nº facturas
        f.save()        
    return "%s: %s Pagos cargadas" % (year, count)

#========================================

def ac_importar_ejercicio(modeladmin, request, queryset, pieza=None):

    for td_cv in queryset:
        emp = td_cv.empresa
        if not emp.fichero:
            mensaje = "No se ha definido fichero de datos"
            modeladmin.message_user(request, mensaje)
            continue
        if td_cv.bloqueado:
            mensaje = "Ejercicio %s bloqueado. \n" % td_cv.alias
            modeladmin.message_user(request, mensaje)
            continue
        fichero = emp.fichero.path
        book = xlrd.open_workbook(fichero)
        sh = book.sheet_by_name(td_cv.alias)
        #------------------------
        mensaje = import_tarifa(sh, td_cv)
        modeladmin.message_user(request, mensaje)
        #-------------------------------
        mensaje = import_peso(sh, td_cv)
        modeladmin.message_user(request, mensaje)
        #-----------------------------
        mensaje = import_sales(sh, td_cv)
        modeladmin.message_user(request, mensaje)
        #-----------------------
        mensaje = import_pays(sh, td_cv)
        modeladmin.message_user(request, mensaje) 
    return
ac_importar_ejercicio.short_description = "2.- IMPORTAR Año"

#---------------------------
def importar_seccion(modeladmin, request, queryset, pieza=None):
    for td_cv in queryset:
        emp = td_cv.empresa
        if not emp.fichero:
            mensaje = "No se ha definido fichero de datos"
            modeladmin.message_user(request, mensaje)
            continue
        if td_cv.bloqueado:
            mensaje = "Ejercicio %s cerrado. \n" % td_cv.alias
            modeladmin.message_user(request, mensaje)
            continue
        fichero = emp.fichero.path
        book = xlrd.open_workbook(fichero)
        sh = book.sheet_by_name(td_cv.alias)
        if pieza:
            mensaje = pieza(sh, td_cv)
            modeladmin.message_user(request, mensaje)
        else:
            mensaje = "No se ha definido funcion"
            modeladmin.message_user(request, mensaje)
    return

def ac_tdcv_importar_tarifa(modeladmin, request, queryset, pieza=None):
    return importar_seccion(modeladmin, request, queryset, pieza=import_tarifa)
ac_tdcv_importar_tarifa.short_description = "2.1.- Importar Tarifa"

def ac_tdcv_importar_factores(modeladmin, request, queryset, pieza=None):
    return importar_seccion(modeladmin, request, queryset, pieza=import_peso)
ac_tdcv_importar_factores.short_description = "2.2.- Importar Factores"

def ac_tdcv_importar_ventas(modeladmin, request, queryset, pieza=None):
    return importar_seccion(modeladmin, request, queryset, pieza=import_sales)
ac_tdcv_importar_ventas.short_description = "2.3.- Importar Ventas"

def ac_tdcv_importar_pagos(modeladmin, request, queryset, pieza=None):
    return importar_seccion(modeladmin, request, queryset, pieza=import_pays)
ac_tdcv_importar_pagos.short_description = "2.4.- Importar Pagos"

