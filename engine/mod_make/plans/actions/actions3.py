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

from mod_admin.utils.base import print_msg,redondea, get_dates_from_period
from mod_auth.companies.models import Company
from mod_auth.doctypes.models import DocType, get_create_doctype
from mod_entity.projects.models import Project, ProjectAux
from mod_make.plans.models import Plan, PlanCV, PlanCVProduct, PlanCVTax




#----------------------------
# Plan
#-------------------------------

#===============================



def delete_plan(plan):
    #-----------------------------
    # borrar cálculos anteriores
    #----------------------
    obj = plan
    PlanCVTax.objects.filter(cv__alias__startswith=obj.alias,
            cv__internal=False).delete()
    PlanCVProduct.objects.filter(cv__alias__startswith=obj.alias,
            cv__internal=False).delete()
    PlanCV.objects.filter(alias__startswith=obj.alias,
            internal=False).delete()
    Plan.objects.filter(alias__startswith=obj.alias,internal=False).update(
            num_int=0, num_dec=0,
            num_int1=0, num_dec1=0, 
            num_int2=0, num_dec2=0, 
            num_int3=0, num_dec3=0,  
    )        
    return

def calculate_months(plan):
    if not plan.children.count():
        return []
    list_plan_month = []
    #------------------
    total_peso = 0
    for plan_mes in plan.children.all().order_by('alias'):
        peso = ProjectAux(trunk=plan.project, inline='PESO', alias=plan_mes.alias).num_int
        total_peso += peso
    if not total_peso:
        return []
    #------------------------
    total_int = 0 # Nº facturas
    for plan_mes in plan.children.all().order_by('alias'):
        peso = ProjectAux(trunk=plan.project, inline='PESO', alias=plan_mes.alias).num_int
        plan_mes.num_int = int(plan.num_int*peso/total_peso + decimal.Decimal(.5))
        total_int += plan.mes.num_int
        # plan_mes.num_dec = 0
        plan_mes.num_int1 = plan.num_int1
        plan_mes.num_dec1 = plan.num_dec1*peso/total_peso
        # plan_mes.num_int2 = plan.num_int2
        # plan_mes.num_dec2 = plan.num_dec2*peso/total_peso
        # plan_mes.num_int3 = plan.num_int3
        # plan_mes.num_dec3 = plan.num_dec3*peso/total_peso
        plan_mes.save()
        list_plan_month.append(plan_mes)
    #------------------------------------
    # ajustar decimales de num facturas
    #-----------------------------
    if plan.num_int != total_int:
        plan_mes.num_int += (plan.num_int-total_int)
        plan_mes.save()
        #----------------------
    return list_plan_month   

def get_peso_dia(plan_day):
    peso = 0
    # num_dia = plan_day.date.day()
    festivos = ProjectAux.objects.filter(trunk=plan_day.project, inline='PESO',
                                        alias__startswith='FIESTA', 
                                        date1=plan_day.date) # , date2__isnull=True
    if festivos.count() > 0:
        peso = festivos[0].num_int
    else:
        vacaciones = ProjectAux.objects.filter(trunk=plan_day.project, inline='PESO',
                                            alias__startswith='FIESTA', 
                                            date1__lte=plan_day.date, date2__gte=plan_day.date)
        if vacaciones.count() > 0:
            peso = vacaciones[0].num_int
        else:
            ds = plan_day.date.weekday()+1
            diasems = ProjectAux.objects.filter(trunk=plan_day.project, inline='PESO',
                                                alias='DIASEM_%s' % ds)
            if diasems.count() > 0:
                peso = diasems[0].num_int
    return decimal.Decimal(peso)

def get_pesos_plan_mes(plan_mes):
    dev = {}
    cero = decimal.Decimal(0.0)
    plan_dias = plan_mes.children.all()
    num_dias_mes = plan_dias.count()
    total_peso_mes_ini = [plan_mes.num_int, plan_mes.num_dec1] # , plan_mes.num_dec2, plan_mes.num_dec3]
    total_peso_mes = [0, cero]
    total_peso_mes_fin = [0, cero]
    #-----------------------------
    for tipo in [0,1]: # ,2,3]:
        total_peso_ini = total_peso_mes_ini[tipo]
        peso_medio = total_peso_ini / num_dias_mes
        # total_peso = 0
        signo = 1 if tipo == 0 else -1
        factor = decimal.Decimal(1.5)
        #--------------------------
        for plan_dia in plan_dias:
            peso = get_peso_dia(plan_dia)
            num_dia = int(plan_dia.alias[-2:])
            if peso > 0:
                peso = decimal.Decimal(peso*100 + signo*num_dia*peso*(tipo+1))*factor
            #-------------------
            dev[plan_dia.alias, tipo] = peso
            total_peso_mes[tipo] += peso
            print_msg('FASE1 %s = %s' % (plan_dia.alias, peso))
        #--------------------------
        for x in range(1, num_dias_mes+1):
            alias =  "%sD%02d" % (plan_mes.alias, x) 
            #-------------------- 
            peso = dev[alias, tipo]
            peso = peso*total_peso_ini/total_peso_mes[tipo]
            if tipo == 0:
                peso = int(redondea(peso, 0))
            else:
                peso = redondea(peso, 2)
            if (peso > 0) and (peso < 1):
                peso = 1
            dev[alias, tipo] = peso
            total_peso_mes_fin[tipo] += peso
            print_msg('FASE2 %s = %s' % (alias, peso))
    return dev

def calculate_days(plan_month):
    cero = decimal.Decimal(0.0)
    # import pdb; pdb.set_trace()
    total_peso_mes_ini = [
        plan_month.num_int, plan_month.num_dec1, plan_month.num_dec2, plan_month.num_dec3]
    pesos_plan_mes = get_pesos_plan_mes(plan_month)
    total_peso_mes_fin = [0, cero, cero, cero]
    #---------------------------
    for plan_day in plan_month.children.all().order_by('alias'):
        peso = pesos_plan_mes[plan_day.alias, 0]
        plan_day.num_int = peso
        total_peso_mes_fin[0] += peso
        #-------------------
        plan_day.num_int1 = plan_month.num_int1
        peso = pesos_plan_mes[plan_day.alias, 1]
        plan_day.num_dec1 = peso
        total_peso_mes_fin[1] += peso
        #-------------------    
        # plan_day.num_int2 = plan_month.num_int2
        # peso = pesos_plan_mes[plan_day.alias, 2]
        # plan_day.num_dec2 = peso
        # total_peso_mes_fin[2] += peso
        # #-------------------
        # plan_day.num_int3 = plan_month.num_int3
        # peso = pesos_plan_mes[plan_day.alias, 3]
        # plan_day.num_dec3 = peso
        # total_peso_mes_fin[3] += peso
        #--------------------------
        plan_day.save()
    #------------------------------
    # aplicar resto procedente de redondeos al dia con má facturas del mes
    #------------------------------
    # import pdb; pdb.set_trace()
    if True:
        plan_day = plan_month.children.all().order_by('-num_int')[0]   
        resto = total_peso_mes_ini[0] - total_peso_mes_fin[0]
        if resto != 0:
            plan_day.num_int += resto
        resto = total_peso_mes_ini[1] - total_peso_mes_fin[1]
        if resto != 0:
            plan_day.num_dec1 += resto
        # resto = total_peso_mes_ini[2] - total_peso_mes_fin[2]
        # if resto != 0:
        #     plan_day.num_dec2 += resto    
        # resto = total_peso_mes_ini[3] - total_peso_mes_fin[3]
        # if resto != 0:
        #     plan_day.num_dec3 += resto    
        plan_day.save()
    return

def ac_generate_planyear(modeladmin, request, queryset, pieza=None):

    count = 0
    for plan in queryset:
        if not plan.locked or not plan.internal: # and plan.level !=1 and plan.level != 2:
            mensaje = "Plan no bloqueado o no interno  %s de nivel %s no se puede calcular" % (plan.alias, plan.level)
            modeladmin.message_user(request, mensaje, messages.WARNING)
            continue
        count +=1
        # import pdb; pdb.set_trace()
        #-------------------
        delete_plan(plan)
        #------------------
        if plan.level == 1:
            list_plan_month = calculate_months(plan)
        elif plan.level == 2:
            list_plan_month = [plan]
        #-------------------- 
        if list_plan_month:
            for plan_month in list_plan_month:     
                calculate_days(plan_month)

        mensaje = "Se ha generado el plan %s \n" % (plan.alias)
        modeladmin.message_user(request,mensaje, messages.SUCCESS)
    return
ac_generate_planyear.short_description = "1.- Generar Plan/Dias"
