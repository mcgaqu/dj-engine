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
from mod_entity.projects.models import Project, ProjectAux
from mod_make.plans.models import Plan, PlanCV, PlanCVProduct

#----------------------------
# Project
#-------------------------------
def create_planyear(project):
    year = int(project.alias)
    doctype = get_create_doctype(project.doctype.company, 'Plan')
    #------------------
    try:
        plan_year = Plan.objects.get(project=project, doctype=doctype, alias=project.alias)
    except Plan.DoesNotExist:
        plan_year = Plan(project=project, doctype=doctype, alias=project.alias)
        plan_year.plan_year_id = plan_year.id
        plan_year.date = datetime.date(year, 1, 1)
        plan_year.internal = True
        plan_year.patron_alias = '&&&&-T-#####'
        plan_year.save()  
    # return plan_year  
    #-------------------
    for trimester in (1,2,3,4):
        mes1 = (trimester*3-2) # (1=enero,4=abril,7=Julio,10=Octubre)
        alias = "%sT%s" % (plan_year.alias, trimester)
        try:
            plan_trim = Plan.objects.get(project=project, parent=plan_year, doctype=doctype, alias=alias)
        except Plan.DoesNotExist:
            plan_trim = Plan(project=project, parent=plan_year, doctype=doctype, alias=alias)
        plan_trim.plan_year_id = plan_year.id
        # plan_trim.project = project
        plan_trim.date = datetime.date(year, mes1, 1)
        # plan_trim.internal = True
        plan_trim.patron_alias = '&&&&-T-#####'
        plan_trim.save()                     
        #---------------------
        for mes in (mes1, mes1+1, mes1+2):
            alias = "%sM%02d" % (plan_trim.alias, mes)
            try:
                plan_mes = Plan.objects.get(project=project, parent=plan_trim, doctype=doctype, alias=alias)
            except Plan.DoesNotExist:
                plan_mes = Plan(project=project, parent=plan_trim, doctype=doctype, alias=alias)
            plan_mes.plan_year_id = plan_year.id
            # plan_mes.project = project
            plan_mes.date = datetime.date(year, mes, 1)
            # plan_mes.internal = True
            plan_mes.save()                     
            #-----------------------
            days = calendar.monthrange(year, mes)[1] # devuelve el dia de la semana del primero de mes y num dias
            for day in range(1, days+1): # days: # range(1, days)
                alias = "%sD%02d" % (plan_mes.alias, day)
                try:
                    plan_day = Plan.objects.get(project=project, parent=plan_mes, doctype=doctype, alias=alias)
                except Plan.DoesNotExist:
                    plan_day = Plan(project=project, parent=plan_mes, doctype=doctype, alias=alias)
                plan_day.plan_year_id = plan_year.id
                # plan_day.project = project
                plan_day.date = datetime.date(year, mes, day)
                # plan_day.internal = True
                plan_day.mark = "%s" % datetime.date(year, mes, day).weekday()
                plan_day.save() 
    return plan_year                    


def add_project_sales(plan):
    project = plan.project
    anyo = project.alias
    dt_plan = get_create_doctype(project.doctype.company, 'Plan')
    dt_plancv = get_create_doctype(project.doctype.company, 'PlanCV')
    niveles = {'A':0, 'T':1, 'M':2, 'D':3}
    count = 0
    
    params = project.datax_set.filter(inline='VENTA')
    for param in params:
        count +=1
        plan = Plan.objects.get(doctype=dt_plan, project=project, alias=param.alias)
        plan.num_int = param.num_int # nº facturas
        plan.num_int1 = param.num_int1 # tipo iva
        plan.num_dec1 = param.num_dec1 # importe venta
        plan.num_int2 = param.num_int2 
        plan.num_dec2 = param.num_dec2 # 
        plan.num_int3 = param.num_int3 
        plan.num_dec3 = param.num_dec3 # 
        plan.num_dec = param.num_dec # pagos
        plan.internal = True
        plan.locked = True
        plan.save()
        #---------------------------------
        if False:
            try:
                cv = PlanCV.objects.get(doctype=dt_plancv, project=project, alias=param.alias)
            except PlanCV.DoesNotExist:
                cv = PlanCV(doctype=dt_plancv, project=project, alias=param.alias)
                cv.active = False
                cv.save()
            if param.num_dec1 != 0:
                try:
                    cvp = PlanCVProduct.objects.get(cv=cv, alias='Venta_tipo1')
                except PlanCVProduct.DoesNotExist:
                    cvp = PlanCVProduct(cv=cv, alias='Venta_tipo1')
                cvp.units = param.num_dec1
                cvp.porc_tax = decimal.Decimal(param.num_int1)
                cvp.price = 1
                cvp.save()
            if param.num_dec2 != 0:
                try:
                    cvp = PlanCVProduct.objects.get(cv=cv, alias='Venta_tipo2')
                except PlanCVProduct.DoesNotExist:
                    cvp = PlanCVProduct(cv=cv, alias='Venta_tipo2')
                cvp.units = param.num_dec2
                cvp.porc_tax = decimal.Decimal(param.num_int2)
                cvp.price = 1
                cvp.save()
            cv.save_tax()
            cv.save()
    #-------------------
    plans = project.plan_set.filter(internal=0, locked=0)
    for plan in plans:
        plan.save()
    return


def ac_create_planyear(modeladmin, request, queryset, pieza=None):
    count = 0
    for project in queryset:
        if project.locked:
            mensaje = "Projecto %s bloqueado" % project.alias
            modeladmin.message_user(request, mensaje, messages.WARNING)
            continue
        count +=1
        plan_year = create_planyear(project)
        add_project_sales(plan_year)
        mensaje = "Se han creado el plan %s" % (project.alias)
        modeladmin.message_user(request,mensaje, messages.SUCCESS)
    return
ac_create_planyear.short_description = "2.- Crear Planes/Año"



