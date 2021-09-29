import os, time, datetime, decimal, random, calendar
from typing import Counter
# from typing_extensions import ParamSpec, ParamSpecArgs
from django.db.models.aggregates import Count
import openpyxl
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
# from mod_auth.companies.models import Company
# from mod_auth.doctypes.models import DocType
from mod_make.plans.models import (
    Plan, PlanFactor, PlanFactorAux, PlanDoc, PlanDocProduct, PlanDocTax)


def get_prioridad(fv):
    if fv.fecha1 != None and not fv.fecha2 and not fv.marca:
        return 0
    if fv.fecha1 != None and fv.fecha2 != None:
        if not fv.marca:
            return 2
        else:
            return 1
    return 3

def get_porc_trimester(plan_year, trimester):
    factor = plan_year.parent.factor
    xs_year = factor.datax_set.filter(inline="PESO", grade="MES")
    total_peso = xs_year.aggregate(Sum('num_int'))['num_int__sum']
    xs_trimester = xs_year.filter(alias__startswith="T%s" % trimester)
    peso_trimester = xs_trimester.aggregate(Sum('num_int'))['num_int__sum']
    porc_trimester = int(peso_trimester*100/total_peso)
    return porc_trimester

def get_porc_month(plan_trimester, month): # % del mes respecto a su trimestre
    factor = plan_trimester.parent.parent.factor
    t = int(plan_trimester.alias[5:6])
    xs_t = factor.datax_set.filter(inline="PESO", grade="MES", alias__startswith="T%s" % t)
    total_peso = xs_t.aggregate(Sum('num_int'))['num_int__sum']
    peso_mes = xs_t.get(alias="T%sM%2d" % (t, month)).num_int
    porc_mes = int(peso_mes*100/total_peso)
    return porc_mes

def get_porc_day(plan_month, day):
    factor = plan_month.parent.parent.parent.factor
    # 1.- obtener factores peso de diasem y diax 
    xs_ds = factor.datax_set.filter(inline="PESO", grade="DIASEM")
    xs_dx = factor.datax_set.filter(inline="PESO", grade="DIAX")
    #-------------
    y = int(plan_month.alias[0:4])
    m = int(plan_month.alias[7:9])
    total_peso = 0
    peso_day = 0
    for d in range(calendar.monthrange(y, m)[0]):
        date = datetime.date(y,m,d)
        fdiax = xs_dx.filter(date1__gte=date, date2_lte=date)
        if fdiax.count():
            peso = fdiax[0].num_int
        else:
            diasem = date.weekday()
            peso = xs_ds.get(alias="DS%s" % diasem).num_int
        total_peso += peso
        if d == day:
            peso_day = peso
    porc_day = int(peso_day*100/total_peso)
    return porc_day
  

def compute_child(plan):
    if plan.nivel == 1: # year --> trimesters
        for t in [1,2,3,4]:
            alias = '%sT%s' % (plan.alias, t)
            peso = get_porc_trimester(plan, t)
    elif plan.nivel == 2: # trimester --> months
        t = int(plan.alias[5:6])
        for m in [1,2,3]:
            alias = '%sM%02d' % (plan.alias, ((t-1)*3+m))
            peso = get_porc_month(plan, (t-1)*3+m)
    elif plan.nivel == 3: # month --> days
        y = int(plan.alias[0:4])
        m = int(plan.alias[7:9])
        ds = calendar.monthcalendar(y,m)[0]
        for d in ds:
            alias = '%sD%02d' % (plan.alias, d)
            peso = get_porc_day(plan, d)
    else:
        pass
    if not plan.locked:
        pp = plan.parent
        plan.num_int = int(pp.num_int*peso + decimal.Decimal(.5))
        plan.num_int1 = pp.num_int1
        plan.num_dec1 = pp.num_dec1 * peso
        plan.num_int2 = pp.num_int2
        plan.num_dec2 = pp.num_dec2 * peso
        plan.num_int3 = pp.num_int3
        plan.num_dec3 = pp.num_dec3 * peso
        plan.locked = True
        plan.internal = True
        plan.date1 = get_dates_from_period(plan.alias)[0]
        plan.date2 = get_dates_from_period(plan.alias)[1]
        plan.save()
    return plan

def compute_resto(plan):
    # sum_entero1 = xs.aggregate(Sum('entero1'))['entero1__sum']
    total = plan.children.agregate(Sum('num_int'))['num_int__sum']
    if plan.num_int != total :
        x = plan.children.order_by('-num_int')[0] # falta algo por asignar --> A asignarlo al más grande
        resto = plan.num_int - total
        x.num_int = x.num_int + resto
        x.save()
    return

def compute_planyear(plan_year):
    #-----------
    fventas = plan_year.factor.datax_set.filter(inline="VENTA")
    for fventa in fventas:
        plan = Plan.objects.get(plan_year_id=plan_year.id, alias=fventa.alias)
        plan.num_int = fventa.num_int
        plan.num_int1 = fventa.num_int1
        plan.num_dec1 = fventa.num_dec1
        plan.num_int2 = fventa.num_int2
        plan.num_dec2 = fventa.num_dec2
        plan.num_int3 = fventa.num_int3
        plan.num_dec3 = fventa.num_dec3
        plan.locked = True
        plan.internal = True
        plan.date1 = get_dates_from_period(fventa.alias)[0]
        plan.date2 = get_dates_from_period(fventa.alias)[1]
        plan.save()
    #---------------
    # calcular descendentes
    #-----------
    plans = Plan.objects.filter(plan_year_id=plan_year.id, locked=True)
    for plan in plans:
        if 'D' in plan.alias:
            pass
        elif 'M' in plan.alias:
            for plan_day in plan.children:
                compute_child(plan_day)
            compute_resto(plan)
        elif 'T' in plan.alias:
            for plan_month in plan.children:
                compute_child(plan_month)
                for plan_day in plan_month.children:
                    compute_child(plan_day)
                compute_resto(plan_month)
            compute_resto(plan)
    #----------
    # recalcular acumulados hacia arriba
    #------------
    plans = Plan.objects.filter(plan_year_id=plan_year.id, locked=True).order_by('level')
    for plan1 in plans:
        if plan1.parent.locked or plan1.parent.internal:
            continue
        plan = plan1.parent
        total = plan1.children.agregate(Sum('num_int'))['num_int__sum']
        plan.num_int = plan.children.agregate(Sum('num_int'))['num_int__sum']
        plan.num_int1 = plan1.num_int1
        plan.num_dec1 = plan.children.agregate(Sum('num_dec1'))['num_dec1__sum']
        plan.num_int2 = plan1.num_int2
        plan.num_dec2 = plan.children.agregate(Sum('num_dec2'))['num_dec2__sum']
        plan.num_int3 = plan1.num_int3
        plan.num_dec3 = plan.children.agregate(Sum('num_dec3'))['num_dec3__sum']
        plan.locked = True
        plan.internal = True
        plan.date1 = get_dates_from_period(plan.alias)[0]
        plan.date2 = get_dates_from_period(plan.alias)[1]
        plan.save()
    return plan_year



def ac_generate_planyear(modeladmin, request, queryset, pieza=None):
    count = 0
    for plan in queryset:
        if plan.locked or plan.level != 1:
            mensaje = "Plan %s bloqueado o nivel != 1. \n" % plan.alias
            modeladmin.message_user(request, mensaje, messages.WARNING)
            continue
        count +=1
        compute_planyear(plan)
        mensaje = "Se han calculado el ejercicios %s" % (plan.alias)
        modeladmin.message_user(request,mensaje, messages.SUCCESS)
    return
ac_generate_planyear.short_description = "1.2.- Calcular Años"
