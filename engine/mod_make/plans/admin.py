import xlrd, xlwt
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import format_html
from django.contrib import messages
from django.db.models import Sum
from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib.auth.models import Group
from mod_admin.main1.options import (ModelAdmin1, ModelLin1,
                                     ModelAuxAdmin1, ModelAuxLin1,
                                     GenericLin1)

from mod_auth.companies.admin import CompanyAdmin1
from mod_auth.doctypes.models import DocType, get_create_doctype
from mod_entity.projects.models import Project, ProjectAux
from mod_entity.projects.admin import ProjectAdmin1, ProjectAuxAdmin1


from .actions import get_app_actions
from .models import Plan, PlanCV, PlanCVProduct, PlanCVTax
from .adminextra import PlanAdmin1Extra, PlanCVAdmin1Extra

class PlanCompanyAdmin1(CompanyAdmin1):
    actions = get_app_actions('Company')

    def AU_projects(self, obj):
        dt = get_create_doctype(obj, 'Project')
        num_projects = Project.objects.filter(doctype=dt).count()
        href = "/%s/projects/project/?doctype__id=%s" % (settings.SITE_NAME, dt.id)
        return format_html('<a href="{}">( {} ) IR</a>', href, num_projects)
    AU_projects.short_description = _("Projects") 

    fieldsets = [
		(None, {
			'fields': [	
                ('alias',  'address'),
                ('tin', 'zipcode'),
				('name', 'city'),
                ('email', 'state'),
                ('tel', 'avatar'),
                ('file'),
                ('AU_projects'),
            ]
		}), 
	]
    readonly_fields = ['AU_projects']

#------------------------------
# PlanProject
#------------------------

class PlanProjectAuxAdmin1(ProjectAuxAdmin1):
    model = ProjectAux
    list_display = ['trunk',
        'inline', 'alias', 'name', 
        'num_int', 'num_dec',
        'grade', 'mark',
        'num_int1', 'num_dec1',
        # 'num_int2', 'num_dec2',
        # 'num_int2', 'num_dec2',
        'date1', 'date2'
    ]
    list_filter = ['trunk', 'inline']


class PlanProjectAuxLin1(ModelAuxLin1):
    model = ProjectAux
    fields = ['line', 'alias', 'name', 'grade', 'sort']

class PlanProjectAuxTarifaLin1(ModelAuxLin1):
    model = ProjectAux
    tab_label = "TARIFA"
    verbose_name_plural = tab_label

    labels = {
        'num_dec': 'precio',
        'num_int': 'peso',
        'grade': 'grupo(B/C)',
        'mark': 'tipo iva',
        'num_int1': 'variacion'
    }  
    
    fields = ['line', 'alias', 'name', 'num_dec', 'num_int', 'grade', 'mark']

class PlanProjectAuxPesoLin1(ModelAuxLin1):
    model = ProjectAux
    tab_label = "PESO"    
    verbose_name_plural = tab_label
    labels = {
        'alias': 'periodo',
        'num_int': 'peso',

    }  
    

    fields = ['line', 'alias', 'name', 'num_int', 'date1', 'date2']

class PlanProjectAuxVentaLin1(ModelAuxLin1):
    model = ProjectAux

    tab_label = "VENTA"
    verbose_name_plural = tab_label
    labels = {
        'alias': 'YYYYT0M00D00',
        'num_int': 'N.Ftras',
        'num_int1': '%IVA1',
        'num_dec1': 'Importe1',
        'num_int2': '%IVA2',
        'num_dec2': 'Importe2',
        'num_int3': '%IVA3',
        'num_dec3': 'Importe3',
    }  
    

    fields = ['line', 'alias', 'num_int', 'num_int1', 'num_dec1', 
        'num_int2', 'num_dec2', 'num_int3', 'num_dec3',
        ]

class PlanProjectAuxPagoLin1(ModelAuxLin1):
    model = ProjectAux
    tab_label = "PAGO"
    verbose_name_plural = tab_label
    labels = {
        'alias': 'periodo',
        'num_dec': 'importe',
        'grade': 'datafono',
        'mark': 'tipo iva',
    }
    fields = ['line', 'alias', 'grade', 'num_dec']



class PlanProjectAdmin1(ProjectAdmin1):
    model = Project

    def AU_plans(self, obj):
        href = "/%s/plans/pplan/?project__id=%s" % (settings.SITE_NAME, obj.id)
        return format_html('<a href="{}">({}) IR</a>', href, 'Projects')
    AU_plans.short_description = _("Plans") 

    list_display = ['alias', 'MU_projectaux', 'MU_plans_internal', 'MU_plan0']
    fields = ['alias','MU_projectaux', 'MU_plans_internal',  'MU_plan0']
    readonly_fields = ['MU_projectaux', 'MU_plans_internal', 'MU_plan0']
    fieldsets = None
    actions = get_app_actions('Project')
    inlines = [# PlanProjectAuxLin1, 
    PlanProjectAuxTarifaLin1, PlanProjectAuxPesoLin1,
    PlanProjectAuxVentaLin1, PlanProjectAuxPagoLin1
    ]



#------------------------------
# Plan
#------------------------
class PlanChildLin1(ModelLin1):
    model = Plan
    fields = ['alias', 'name',  'grade', 'sort']


class PlanAdmin1(ModelAdmin1, PlanAdmin1Extra):
    model = Plan
    ordering = ('alias',)	
    date_hierarchy = 'date1'

    list_display = [# 'level',
        'MU_Project', # 'doctype', 
		'alias', 'locked', 'internal',
		'MC_date', 'MC_date_diasem',# 'ME_date_trimestre',
        'num_int', 'EB_ok1',
        'EE_sum_numftras_plan', 
		'EE_sum_cvs',
		'EC_cvs_ini_fin_sort',
		'EC_cvs_ini_fin_alias',
        # #-------------------
        'num_int1', 'num_dec1', 
        #     'ED_tax1', 'ED_total1',
                 'ED_sum_base1_plan', 'ED_sum_base1_cvs', 
        #         'ED_sum_tax1_plan', 'EEDsum_tax1_cvs', 
        # 'num_int2', 'num_dec2',
        #     'ED_tax2', 'ED_total2',
        #         'ED_sum_base2_plan', 'AD_sum_base2_cvs',
        #         'AD_sum_tax2_plan', 'AD_sum_tax2_cvs',  
        # 'num_int3', 'num_dec3',
        #     'ED_tax3', 'ED_total3',             
        #         'ED_sum_base3_plan', 'ED_sum_base3_cvs',
        #         'ED_sum_tax3_plan', 'ED_sum_tax3_cvs', 
        # #----------------------------- 
        'ED_amount_base','EB_ok2', 
        'ED_amount_base_cvs',# 'ED_amount_tax_cvs', 'ED_amount_total_cvs', 
        # #----------------------------- 
        # 'num_dec',
        #    'ED_suma_paid_plan', 'ED_suma_paid_cvs',
        # #-----
        # 'EB_ok1' # num facturas plan == num ftras generadas
        # 'EB_ok2', # importe base plan == importe base facturas generadas
        # 'EB_0k3' # importe pago tarjeta plan (num_dec) < total ftras generadas('AD_amount_total)
        'EB_ok_all' ,# oke1 && ok2 && ok3
        # #------------------------
        ]
    list_display_links = list_display
    list_editable = []
    list_filter = ['level', 'internal','locked', 'project']
    search_fields = ('^alias', 'name',)

    fields = list_display
    fieldsets = [
		(None, {
			'fields': [# 'level',
        'MU_Project', 'alias', 'locked', 'internal',
		# 'MC_date1_diasem', 'MC_date1_trimestre',
        'num_int', 'EB_ok1',
        #     'EE_sum_numftras_plan', 'EE_sum_cvs',
        # #-------------------
        'num_int1', 'num_dec1', 
        #     'AD_base1', 'AD_tax1', 'AD_total1',
        #         'AE_sum_base1_plan', 'AE_sum_base1_cvs', 
        #         'AE_sum_tax1_plan', 'AE_sum_tax1_cvs', 
        'num_int2', 'num_dec2',
        #     'AD_base2', 'AD_tax2', 'AD_total2',
        #         'AE_sum_base2_plan', 'AE_sum_base2_cvs',
        #         'AE_sum_tax2_plan', 'AE_sum_tax2_cvs',  
        # 'num_int3', 'num_dec3',
        #     'AD_base3', 'AD_tax3', 'AD_total3',             
        #         'AE_sum_base3_plan', 'AE_sum_base3_cvs',
        #         'AE_sum_tax3_plan', 'AE_sum_tax3_cvs', 
        # #----------------------------- 
        'ED_amount_base','EB_ok2', 
        # 'ED_amount_base_cvs', 'ED_amount_tax_cvs', 'ED_amount_total_cvs', 
        # #----------------------------- 
        'num_dec',
        #    'ED_suma_paid_plan', 'ED_suma_paid_cvs',
        # #-----
        # 'EB_ok1' # num facturas plan == num ftras generadas
        # 'EB_ok2' # importe total plan == importe total facturas generadas
        # 'EB_0k3' # importe pago tarjeta plan (num_dec) < total ftras generadas('AD_amount_total)
        'EB_ok_all' # oke1 && ok2 && ok3
        # #------------------------
        ]
		}), 
	]
    readonly_fields = ['MU_Project', 'EB_ok1', 'ED_amount_base', 'EB_ok2', 'EB_ok_all']

    inlines = [PlanChildLin1]
    actions = get_app_actions('Plan')



#------------------------------
# PlanCV
# -----------------
class PlanCVAdmin1(ModelAdmin1):
	list_display = ['alias', 'date1', 'sort', 'amount_base', 'amount_tax', 'amount_total']
	search_fields = ['^alias']
	# actions = get_app_actions('Invoice')


class PlanCVProductAdmin1(ModelAdmin1):
    # actions = get_app_actions('Invoice')
	list_display = ['CD_price_base', 'product', 'cv', 'alias', 'units', 'price', 'tax_included', 'porc_tax', 
						'amount_base', 'amount_tax', 'amount_total']

class PlanCVTaxAdmin1(ModelAdmin1):
    # actions = get_app_actions('Invoice')
	list_display = ['alias', 'grade', 'sort', 'cv', 'porc_tax', 'amount_base', 'amount_tax']




if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Plan)

"""
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import decimal
from functools import update_wrapper
from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse

from escala.admin1.actions import ac_export_csv, ac_export_pdf, ac_export_xls

from escala.admin1.adms import (Menu1Class,
								Admin1Model,
								TabularLIn,
								Admin1TreeTPD,
								Admin1TipoDocBase)

from escala.admin1.adms.tpd import Admin1TPD
from escala.admin1.filters import  NivelFilter, TipoDocFilter
from escala.utils.base import redondea, print_msg

from escala.e1empresa.models import Empresa
from escala.e1empresa.actions import ac_emp_copia_seguridad
from escala.e2tipodocs.models import TipoDoc, get_crear_tipodoc

from multierp.m0base1.models import Factor, FactorValor
from multierp.m2productos.models import Producto

from multierp.m3tareas.models import Tarea
from multierp.m4cv.models import CV, CVProducto , CVTasa
from multierp.m5pagos.models import Pago, PagoD

from xapps.e1empresa.admin1 import Admin1Empresa, EmpresaXLIn, Admin1EmpresaX

from xapps.plan_negocio.models1 import def_Admin1PlaNTipoDocCV
from xapps.plan_negocio.models1 import ExtraAdmin1TipoDocCV # , ExtraAdmin1CV
from xapps.plan_negocio.models1 import ExtraAdmin1CVI # , ExtraAdmin1CVE





#---------------------------------
# FactorValor
#--------------------------

def def_Admin1PlaNFactorValor():
	return {
		'campos': {
			'entero': {'etiq_form': 'Prioridad', 'etiq_list': 'Proridad'},
			'marca': {'etiq_form': 'Dia Semana / Mes', 'etiq_list': 'Dia Sem/Mes'},
			'entero1': {'etiq_form': '% Ventas', 'etiq_list': '% Ventas'},
			'factor': {'etiq_form': 'Año', 'etiq_list': 'Año'},
		}
	}

class Admin1PlaNFactorValor(Admin1Model):
	model = FactorValor
	list_display = ('factor', 'entero', 'alias',
					'grupo', 'marca',
					'entero1', 'fecha1', 'fecha2')	

	list_display_links = list_display
	list_editable = ('entero1',)
	list_filter = ('factor', 'grupo') 
	date_hierarchy = 'fecha1'

	fieldsets = [
		(None, {
			'fields': ('factor', 'entero', 'alias',
					   'grupo', 'marca',
					   'entero1', 'fecha1', 'fecha2')	
		}), 
	]

	def save_model(self, request, obj, form, change):
		obj.entero = get_prioridad(obj)
		return super(Admin1PlaNFactorValor, self).save_model(
					request, obj, form, change)


#--------------------------
# Productos
#-----------------------
	
def def_Admin1PlaNProducto():
	return {
		'campos': {
			'entero': {'etiq_form': '% Venta', 'etiq_list': '% Venta'},
			'orden': {'etiq_form': '% Var.Precio', 'etiq_list': '% Var.Precio'},
			'tipodoc': {'etiq_form': 'Año', 'etiq_list': 'Año'},
			#'TipoDocFilter': {'etiq_form': 'Ejercicio', 'etiq_list': 'Ejercicio'},
			'precio_ingreso': {'etiq_form': 'Precio Venta', 'etiq_list': 'Precio Venta'},
			'CC_fecha1': {'etiq_form': 'Desde Fecha', 'etiq_list': 'Desde Fecha'},
			'fecha1': {'etiq_form': 'Desde Fecha', 'etiq_list': 'Desde Fecha'},
			'CC_fecha2': {'etiq_form': 'Hasta Fecha', 'etiq_list': 'Hasta Fecha'},
			'fecha2': {'etiq_form': 'Hasta Fecha', 'etiq_list': 'Hasta Fecha'},
		},
	}                    

   
class Admin1PlaNProducto(Admin1TreeTPD):
	model = Producto
	list_display = ('tipodoc', 'grupo', 'CC_fecha1', 'CC_fecha2', 'alias',
					'nombre','precio_ingreso', 'entero', 'orden','tasa',
					'CE_num_cvps', 'activo')

	list_display_links = ('tipodoc', 'grupo', 'CC_fecha1', 'CC_fecha2', 'alias',
					'nombre', 'precio_ingreso')
	list_editable = ('entero', 'orden')
	list_filter = (# 'TipoDocFilter','tasa',
				   'activo', 'grupo')
	date_hierarchy = 'fecha1'
	
	fieldsets = [
		(None, {
			'fields': ('tipodoc', 'grupo', 'fecha1', 'fecha2', 'alias',
					'nombre','precio_ingreso', 'entero', 'orden', 'tasa', 'activo')
			}),
		]    


#--------------------------
# Prevision de Ventas
#-----------------------

def def_Admin1PlaNTipoDocCVI():
	return def_Admin1PlaNTipoDocCV()


class Admin1PlaNTipoDocCVI(Admin1TipoDocBase, ExtraAdmin1TipoDocCV):
	model = TipoDoc
	nombre1 = "Año"
	filtro = {'interno':False, 'tabla__alias':'CV'}
	list_display = ('alias', #'entero',
					'marca', # 'orden',
					'CH_admin1_url1', 'CH_admin1_url2', 'CH_admin1_url8',
					'CE_entero1', # 'CE_entero2',
					'CH_total_ventas', 'CH_importe_pagado',
					'CH_precio_medioB', 'CH_importe_medio',
					'CH_admin1_url3', 'CH_admin1_url4',
					#'CE_num_cvs', 'CE_num_cvps',
					'CL_completo','bloqueado',
					)

	list_display_links = ('alias', 'bloqueado',	'entero', 'marca',)

	fieldsets = [(None, {'fields': ('alias', 'marca', 'bloqueado')})]
	readonly_fields = ('alias',)

	def has_add_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj):
		return False
	
	actions = (ac_tdcv_crear_ejercicios,
				ac_tdcv_importar_ejercicio,
				ac_tdcv_importar_tarifa,
				ac_tdcv_importar_factores,
				ac_tdcv_importar_ventas,
				ac_tdcv_importar_pagos,
				#---------------------
				ac_tdcv_eliminar_ejercicios,
				# ac_tdcv_informes
				)

#-------------------------------------

class CVTasaLIn(TabularLIn):
	model = CVTasa
	verbose_name_plural = "Impuestos"
	fields = ('lin', 'importe_base', 'CH_porc_iva',  'CH_importe_iva' )
	readonly_fields = fields
	can_delete = False

	def has_add_permission(self, request):
		return False

class CVProductoTasaLIn(TabularLIn):
	model = CVProducto
	verbose_name_plural = "Ventas por Tipo de Iva"
	fields = ('lin', 'precio', 'tasa', 'CH_cuota_tasa')
	readonly_fields = ('CH_cuota_tasa',)


class CVProductoLIn(TabularLIn):
	model = CVProducto
	verbose_name_plural = "Productos"
	fields = ('lin', 'producto', 'unidades', 'precio',
			  'iva_incluido', 'tasa', 'importe_base')
	readonly_fields = ('importe_base')
	# raw_id_fields = ('producto')

#--------------------------
# Admin1PlanCV1: Entrada de ventas por periodo
#-----------------------
def def_Admin1PlaNCV1():
	return {
		'campos': {
			'tipodoc': {'etiq_form': 'Año', 'etiq_list': 'Año'},
			'alias': {'etiq_form': 'Periodo', 'etiq_list': 'Periodo'},
			'entero': {'etiq_form': 'Peso', 'etiq_list': 'Peso'},
			'orden': {'etiq_form': '1ª Ftra', 'etiq_list': '1ª Ftra'},
			'CC_fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			#--------------------
			'bloqueado': {'etiq_form':'Manual', 'etiq_list':'Manual'},
			'entero1': {'etiq_form': 'Ftras Previstas', 'etiq_list': 'Ftras Previstas'},
			'entero2': {'etiq_form': 'Nº F.Prev2', 'etiq_list': 'Ftras Prev2'},
		},
		'inlines': {
			'CVProductoTasaLIn': {
				'campos': {
					'precio': {'etiq_list': 'Base Imponible', 'attrs': {'class':'.v5TextField',},},
					'CD_cuota_tasa': {'etiq_form':'IVA', 'etiq_list':'IVA'},
					'tasa': {'etiq_form':'Tipo IVA', 'etiq_list':'Tipo IVA'}
				},
			}
		}
	}


class Admin1PlaNCV1(Admin1TreeTPD, ExtraAdmin1CVI):

	model = CV
	def get_queryset(self, request):
		qs = super(Admin1PlaNCV1, self).get_queryset(request)
		qs = qs.filter(interno=True, nivel__lte=2)
		return qs

	sufijo_url = "?bloqueado=0"
	ordering = ('alias',)	
	search_fields = ('^alias', 'orden',)
	date_hierarchy = 'fecha1'

	list_display = ('alias', 'bloqueado', 'entero', 
					'CE_entero1',# 'CE_entero2',
					'CH_total_base','CH_total_tasa', 'CH_total_facturar',
					'CL_ok1', 'CL_ok2', 'CL_ok3',
					'CL_todo_ok')
	
	list_display_links =  ('alias',)
	list_editable = ('bloqueado',)
	
	fieldsets =  [
		(None, {'fields': [('alias', 'bloqueado'),
						   ('entero', 'CH_total_base'),
						   ('orden', 'CH_total_tasa'),
						   ('entero1', 'CH_total_facturar')
		]}),
	]
	readonly_fields = ('alias', 'CH_total_base','CH_total_tasa', 'CH_total_facturar') 

	inlines = [CVProductoTasaLIn]

	
	def has_add_permission(self, request, obj=None):
		return False
	
	def has_delete_permission(self, request, obj):
		return False

	def x_change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')
	
	def x_change_view(self, request, object_id, form_url='', extra_context=None):
		obj = self.get_object(request, unquote(object_id))
		if not obj.bloqueado:
			self.message_user(
				request, "No se puede editar el registro %s. No es Manual" % obj.alias)
			return HttpResponseRedirect('../')
		return super(Admin1PlaNCV1, self).change_view(
			request, object_id, form_url, extra_context)

	#def save_model(self, request, obj, form, change):
	#	super(Admin1PlaNCV1, self).save_model(request, obj, form, change)
	#	obj.save_tasa()
	#	
	#def save_related(self, request, form, formsets, change):
	#	# import pdb; pdb.set_trace()
	#	super(Admin1PlaNCV1, self).save_related(request, form, formsets, change)
	#	form.instance.save_tasa()

#--------------------------
# Admin1PlanCV2: Entrada de facturas
#-----------------------

def def_Admin1PlaNCV2():
	from piezas import xapp_ADMXS, xapp_ARCOS, xapp_INFOS, xapp_DOCXS
	alias = 'Admin1PlanCV2'
	return {
		#'admxs': xapp_ADMXS().get(alias, {}),
		#'docxs': xapp_DOCXS().get(alias, {}),
		'infos': xapp_INFOS().get(alias, {}),
		#'arcos': xapp_ARCOS().get(alias, {}),
		
		'campos': {
			'tipodoc': {'etiq_form': 'Año', 'etiq_list': 'Año'},
			'orden': {'etiq_form': 'Nº Factura', 'etiq_list': 'Nº Ftra'},
			'CD_total_cuota': {'etiq_form':'Cuota', 'etiq_list':'Cuota'},
			'bloqueado': {'etiq_form':'Fijo', 'etiq_list':'Fijo'},
			'total_facturar': {'etiq_form':'Total Factura', 'etiq_list':'Total Factura'},
			'marca': {'etiq_form':'Forma de Pago', 'etiq_list':'Forma de Pago',
					  'definido': 'formaPago'},
			'fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			'CC_fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
		},
		#------------------------------------------------------------
		'inlines': {
			'CVProductoLIn': {
				'campos': {
					# 'precio': {'etiq_list': 'Ingresos', 'attrs': {'class':'.v5TextField',},},
					'CD_cuota_tasa': {'etiq_form':'Cuota', 'etiq_list':'Cuota'},
					'tasa': {'etiq_form':'Tipo IVA', 'etiq_list':'Tipo IVA'}
				},
			},
			'CVTasaLIn': {
				'campos': {
					'orden': {'attrs': {'class':'.v5TextField',},},
					'alias': {'attrs': {'class':'.v10TextField', },},
					'grupo': {'attrs': {'class':'.v5LargeTextField',},},
					'nombre': {'attrs': {'class':'.v10TextField',},},
				},
			}
		}
	}


class Admin1PlaNCV2(Admin1TreeTPD, ExtraAdmin1CVI):
	model = CV
	nombre1 = "Venta Fija"
	def get_queryset(self, request):
		qs = super(Admin1PlaNCV2, self).get_queryset(request)
		qs = qs.filter(interno=True, alias__contains="X")
		return qs
	ordering = ('alias',)	
	search_fields = ('^alias', 'orden',)
	date_hierarchy = 'fecha1'	
	list_display = ('tipodoc', 'alias', 'orden', 'fecha1', 'marca', 'CH_total_base',
					'CH_total_tasa', 'CH_total_facturar', 'CH_total_pagado')
	
	list_display_fields = list_display
	list_filter = ('marca', 'bloqueado', 'fecha1')
	fieldsets =  [
		(None, {'fields': [
			# ('tipodoc','alias', 'bloqueado'),
			('fecha1', 'CH_total_base'),
			('orden', 'CH_total_tasa'),
			('marca', 'CH_total_facturar'),
		]}),
	]
	
	fieldsets =  [
		(None, {'fields': [
			# ('tipodoc','alias', 'bloqueado'),
			('fecha1', 'orden'),
			('CH_total_base', 'CH_total_tasa', 'CH_total_facturar'),
		]}),
	]
	readonly_fields = ('alias', 'total_base', 'CH_total_base','CH_total_tasa', 'CH_total_facturar',
					'CH_total_pagado',)
	# raw_id_fields = ('tercero', 'agente')        

	inlines = [CVProductoLIn, CVTasaLIn]
	actions = [ac_CVpdf]

	def get_urls(self):
		from django.conf.urls import url
		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)
		info = self.model._meta.app_label, self.model._meta.model_name
		urlpatterns = super
		urlpatterns = [
			url(r'^(.+)/pon_precio/$', wrap(self.pon_precio), name='%s_%s_pon_precio' % info),
			]
		return urlpatterns + super(Admin1PlaNCV2, self).get_urls()

	def pon_precio(self, request, id):
		producto_id = request.GET.get("producto_id")
		origen = request.GET.get("origen")
		producto = Producto.objects.get(id=int(producto_id))
		return HttpResponse("%s///%s" % (origen, producto.precio_ingreso))
	


	def save_model(self, request, obj, form, change):
		if obj.fecha1:
			obj.tipodoc = TipoDoc.objects.get(
				tabla__alias="CV", alias="%s" % obj.fecha1.year)
			obj.alias = alias = "%sT%sM%02dD%02d_X%s" % (
					obj.fecha1.year, obj.CE_fecha1_trimestre,
					obj.fecha1.month, obj.fecha1.day, obj.id)
		if not obj.bloqueado:
			obj.bloqueado=True
		if not obj.interno:
			obj.interno=True
		return super(Admin1PlaNCV2, self).save_model(request, obj, form, change)
		# obj.save_tasa()




	def save_related(self, request, form, formsets, change):
		super(Admin1PlaNCV2, self).save_related(request, form, formsets, change)
		form.instance.save_tasa()

#--------------------------
# Admin1PlanCV3: Ventas Año-Trimestre-Mes
#-----------------------
def def_Admin1PlaNCV3():
	return {
		'campos': {
			'tipodoc': {'etiq_form': 'Año', 'etiq_list': 'Año'},
			'alias': {'etiq_form': 'Periodo', 'etiq_list': 'Periodo'},
			'entero': {'etiq_form': 'Peso', 'etiq_list': 'Peso'},
			'orden': {'etiq_form': '1ª Ftra', 'etiq_list': '1ª Ftra'},
			'CC_fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			#--------------------
			'bloqueado': {'etiq_form':'Manual', 'etiq_list':'Manual'},
			'entero1': {'etiq_form': 'Ftras Previstas', 'etiq_list': 'Ftras Previstas'},
			'entero2': {'etiq_form': 'Nº F.Prev2', 'etiq_list': 'Ftras Prev2'},
			# 'CE_entero1': {'etiq_form': 'Ftras Previstas', 'etiq_list': 'Ftras Previstas'},
			# 'CE_entero2': {'etiq_form': 'Nº F.Prev2', 'etiq_list': 'Ftras Prev2'},
			#'CH_total_base': {'etiq_form':'Base', 'etiq_list':'Base'},
			#'CH_total_cuota': {'etiq_form':'IVA', 'etiq_list':'IVA'},
			#'CH_total_facturar': {'etiq_form':'Total', 'etiq_list':'Total'},
			##--------------------
			#'CH_total_facturado': {'etiq_form':'Facturado ', 'etiq_list':'Facturado'},
			#'CC_facturas_ini_fin': {'etiq_form':'Rango Facturas', 'etiq_list':'Rango Facturas'}
		},
		'inlines': {
			'CVProductoTasaLIn': {
				'campos': {
					'precio': {'etiq_list': 'Ingresos', 'attrs': {'class':'.v5TextField',},},
					'CD_cuota_tasa': {'etiq_form':'Cuota', 'etiq_list':'Cuota'},
					'tasa': {'etiq_form':'Tipo IVA', 'etiq_list':'Tipo IVA'}
				},
			}
		}
	}


class Admin1PlaNCV3(Admin1TreeTPD, ExtraAdmin1CVI):

	model = CV
	def get_queryset(self, request):
		qs = super(Admin1PlaNCV3, self).get_queryset(request)
		qs = qs.filter(interno=True, nivel__lte=2)
		return qs
	nombre1 = "Cálculos"

	ordering = ('alias',)	
	search_fields = ('^alias', 'orden',)
	date_hierarchy = 'fecha1'

	list_display = ('alias', 'entero', # 'CC_fecha1', 'orden',
					'CE_entero1',# 'CE_entero2',
					#'CH_total_base','CH_total_tasa',
					'CH_total_facturar',
					'CE_num_cvs', 'CE_num_cvps', 'CH_total_facturado',
					'CC_facturas_ini_fin',
					'CH_suma_facturas_pagadas',# 'CD_porc_pago',
					'CH_importe_pagado',
					'CL_ok1', 'CL_ok2', 'CL_ok3', 'CL_ok4',
					 )
	fieldsets = None

	inlines = [] # [CVProductoTasaLIn]
	actions = (ac_calcular_dias, ac_generar_cvs,
				ac_generar_cvproductos,
				ac_renumerar_facturas,
				ac_cv_ajustar_tarjeta,
				ac_cv1_informe_resumen,
				ac_cv1_informes)
	
	def has_add_permission(self, request, obj=None):
		return False
	
	def has_delete_permission(self, request, obj):
		return False

	def change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')


#--------------------------
# Admin1PlanCV4: Ventas Diarias
#-----------------------

def def_Admin1PlaNCV4():
	return {
		'campos': {
			'entero': {'etiq_form': 'Peso', 'etiq_list': 'Peso'},
			'orden': {'etiq_form': '1ª Ftra', 'etiq_list': '1ª Ftra'},
			#'bloqueado': {'etiq_form':'Manual', 'etiq_list':'Manual'},
			'marca': {'etiq_form': 'Dia Semana', 'etiq_list': 'DS'},
			'CC_fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			'CC_fecha1_diasem': {'etiq_form': 'Dia Semana', 'etiq_list': 'Dia Semana'},
		},
	}

class Admin1PlaNCV4(Admin1TreeTPD, ExtraAdmin1CVI):

	model = CV
	def get_queryset(self, request):
		qs = super(Admin1PlaNCV4, self).get_queryset(request)
		qs = qs.filter(interno=True, nivel=3)
		return qs
	nombre1 = 'Ventas Dia'

	list_display = (# 'alias', 'marca',
					'CC_fecha1','CC_fecha1_diasem', 'entero',
					'CE_entero1', # 'entero2',
					'CE_num_cvs', 'CE_num_cvps', 'CH_total_facturado',
					# 'CL_ok1', 'CL_ok2, 'CL_ok3',
					'CC_facturas_ini_fin', 
					'CH_suma_facturas_pagadas', 'CD_porc_pago',
					'CH_importe_pagado',
					'CL_ok1',# 'CL_ok2',
					'CL_ok3', 'CL_ok4', # 'CL_todo_ok'
					'CL_todo_ok'
					)

	date_hierarchy = 'fecha1'
	ordering = ['alias']
	fieldsets = []
	
	def has_add_permission(self, request, obj=None):
		return False
	
	def has_delete_permission(self, request, obj):
		return False

	def change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')
	

#--------------------------
# Admin1PlanCV - Facturas Informes Resultado
#-----------------------

def def_Admin1PlaNTipoDocCVE():
	return def_Admin1PlaNTipoDocCV()


class Admin1PlaNTipoDocCVE(Admin1TipoDocBase, ExtraAdmin1TipoDocCV):
	model = TipoDoc
	filtro = {'interno':False, 'tabla__alias':'CV'}
	
	list_display = ('alias',
					'CE_entero1', # 'CE_entero2',
					'CH_total_ventas', 'CH_importe_pagado',
					'CH_admin1_url5', 'CH_admin1_url6', 'CH_admin1_url7',
					'CH_suma_total_base', 'CH_suma_total_tasa',
					'CH_suma_total_facturar', 
					'CE_num_pagod', 'CH_suma_facturas_pagadas',
					'CL_completo', 'bloqueado',
					)
	actions = ()

	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False
	
	def change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')

#-----------------------------
# Facturas generadas: Externas (Bloqueadas=Manual + No BLoqueadas=Calculadas)
#-------------------------------
	
def def_Admin1PlaNCV():
	from piezas import xapp_ADMXS, xapp_ARCOS, xapp_INFOS, xapp_DOCXS
	alias = 'Admin1PlanCV'
	return {
		'docxs': xapp_DOCXS().get(alias, {}),
		'infos': xapp_INFOS().get(alias, {}),
		'campos': {
			'tipodoc': {'etiq_form': 'Año', 'etiq_list': 'Año'},
			'orden': {'etiq_form': 'Nº Factura', 'etiq_list': 'Nº Ftra'},
			'grupo': {'etiq_form': 'Trimestre', 'etiq_list': 'Trimestre'},
			'bloqueado': {'etiq_form':'Fijo', 'etiq_list':'Fijo'},
			'total_facturar': {'etiq_form':'Total Factura', 'etiq_list':'Total Factura'},
			'marca': {'etiq_form':'Forma de Pago', 'etiq_list':'Forma de Pago'},
			'CC_fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			'CH_total_cuota': {'etiq_form':'IVA', 'etiq_list':'IVA'},
		},
		#------------------------------------------------------------
		'inlines': {
			'CVProductoLIn': {
				'campos': {
					'precio': {'etiq_list': 'Ingresos', 'attrs': {'class':'.v5TextField',},},
					'CD_cuota_tasa': {'etiq_form':'IVA', 'etiq_list':'IVA'},
					'tasa': {'etiq_form':'Tipo IVA', 'etiq_list':'Tipo IVA'}
				},
			},
			'CVTasaLIn': {
				'campos': {
					'orden': {'attrs': {'class':'.v5TextField',},},
					'alias': {'attrs': {'class':'.v10TextField', },},
					'grupo': {'attrs': {'class':'.v5LargeTextField',},},
					'nombre': {'attrs': {'class':'.v10TextField',},},
				},
			}
		}
	}



class Admin1PlaNCV(Admin1TreeTPD, ExtraAdmin1CVI):
	model = CV
	def get_queryset(self, request):
		qs = super(Admin1PlaNCV, self).get_queryset(request)
		qs = qs.filter(interno=False)
		return qs

	list_display = ('grupo', # 'alias',
					'orden', 'CC_fecha1', 'marca', 
					'total_base', 'CH_total_cuota', 'total_facturar', 
					'CE_num_cvps', 'bloqueado')
	list_display_links = list_display
	ordering = ('alias',)
	search_fields = ('^alias', 'orden')
	date_hierarchy = 'fecha1'	

	fieldsets =  [
		(None, {'fields': ['alias',('marca', 'total_base'),
				('orden', 'CD_total_cuota'), ('fecha1', 'total_facturar'), 
		]}),
	]
	readonly_fields = ('alias', 'total_base', 'CD_total_cuota', 'total_facturar')
	inlines = [CVProductoLIn, CVTasaLIn]
	actions = [ac_CVpdf]

	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False
		
	def save_related(self, request, form, formsets, change):
	    # import pdb; pdb.set_trace()
	    super(Admin1PlaNCV, self).save_related(request, form, formsets, change)
	    obj = CV.objects.get(id=form.instance.id)
	    obj.save_tasa()

def def_Admin1PlaNCVTasa():
	return {
		'campos': {
			'fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			'orden': {'etiq_form': 'Nº Factura', 'etiq_list': 'Nº Factura'},
			'alias': {'etiq_form': 'Nº Factura', 'etiq_list': 'Nº Factura'},
			'tasa': {'etiq_form': 'Tipo Iva', 'etiq_list': 'Tipo Iva'},
			'grupo': {'etiq_form': 'Trimestre', 'etiq_list': 'Trimestre'},
			'tasa__porc': {'etiq_form': '% IVA', 'etiq_list': '% IVA'},
		},
	}


class Admin1PlaNCVTasa(Admin1Model):
	
	model = CVTasa
	
	def get_queryset(self, request):
		qs = super(Admin1PlaNCVTasa, self).get_queryset(request)
		qs = qs.filter(cv__interno=False)
		return qs
	
	list_display = ('grupo', 'alias', 'fecha1', 'orden', # 'grupo', 'orden', 'nombre',
					 'importe_base', 'CH_porc_iva', # 'tasa',
					 'importe_iva',)
	list_filter = ('grupo', 'tasa__porc') # trimestre, tasa

	date_hierarchy = 'fecha1'
	ordering = ['cv__orden', 'tasa']
	search_fields = ('grupo', 'cv__orden', 'cv__alias')

	fieldsets =  [(None, {'fields': ['alias']})]

	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False

	def change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')

#-------------------------	

def def_Admin1PlaNCVProducto():
	return {
		'campos': {
			'fecha1': {'etiq_form': 'Fecha', 'etiq_list': 'Fecha'},
			'orden': {'etiq_form': 'Nº Factura', 'etiq_list': 'Nº Factura'},
			'alias': {'etiq_form': 'Nº Factura', 'etiq_list': 'Nº Factura'},
			'tasa': {'etiq_form': 'Tipo Iva', 'etiq_list': 'Tipo Iva'},
			'grupo': {'etiq_form': 'Trimestre', 'etiq_list': 'Trimestre'},
			'tasa__porc': {'etiq_form': '% IVA', 'etiq_list': '% IVA'},
			'producto__grupo': {'etiq_form': 'Grupo de Producto', 'etiq_list': 'Grupo de  Proucto'},
			'CC_producto_grupo': {'etiq_form': 'Grupo de Producto', 'etiq_list': 'Grupo de Producto'},
				
		},
	}
	
class Admin1PlaNCVProducto(Admin1Model):
	model = CVProducto

	def get_queryset(self, request):
		qs = super(Admin1PlaNCVProducto, self).get_queryset(request)
		qs = qs.filter(cv__interno=False)
		return qs
	
	list_display = ('grupo', 'fecha1', 'orden', 'lin', 'producto',
					'CC_producto_grupo', 'unidades', 'precio', # 'tasa',
					'CH_porc_iva','importe_base',)

	list_filter = ('grupo', 'producto__grupo')
	
	date_hierarchy = 'fecha1'
	ordering = ['orden', 'lin']
	search_fields = ['orden', 'producto__alias', 'producto__nombre']

	fieldsets =  [(None, {'fields': ['alias']})]
	inlines = []

	def CC_producto_grupo(self, obj):
		return '' if not obj.producto else obj.producto.grupo
	CC_producto_grupo.short_description = "Grupo de Producto"

	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False

	def change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')	

#-----------------------
# Pagos
#---------------------------

def def_Admin1PlaNTipoDocPago():
	return {
		'campos': {
			'alias': {'etiq_form': 'Año', 'etiq_list': 'Año'},
			'CE_num_regs': {'etiq_form': 'Nº Pagos', 'etiq_list': 'Nº Pagos'},
		},
		'inlines': {
			'PagoLIn': { 
				'campos': {
					'marca': {'etiq_form': 'Forma de Pago', 'etiq_list': 'Forma de Pago',
						'definido': 'formaPago'},
					'fecha1': {'etiq_form': 'Fecha Pago', 'etiq_list': 'Fecha Pago'},
					'fecha2': {'etiq_form': 'Desde Fecha Venta', 'etiq_list': 'Desde Fecha Venta'},
					'fecha3': {'etiq_form': 'Hasta Fecha Venta', 'etiq_list': 'Hasta Fecha Venta'},
				}
			}
		}
	}   

class PagoLIn(TabularLIn):
	model = Pago
	fields = ('marca', 'fecha1', 'importe', 'fecha2', 'fecha3')


class Admin1PlaNTipoDocPago(Admin1TipoDocBase):

	nombre1 = "Pagos"
	filtro = {'interno':False, 'tabla__alias':'Pago'}
	
	list_display = ('alias', 'CH_admin1_url', 'CE_num_regs',
					'CH_admin1_url9',
					'CH_suma_importe', 'CH_suma_asignado', 'CH_suma_pendiente',
					)
	list_display_links = ['alias']
	
	fieldsets =  [(None, {'fields': ['alias']})]
	inlines = [PagoLIn]
	
	def CD_suma_importe(self, obj):
		return obj.pago_set.all().aggregate(Sum('importe'))['importe__sum'] or 0
	def CH_suma_importe(self, obj):
		return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_importe(obj))
	CH_suma_importe.allow_tags = True
	CH_suma_importe.short_description = "Suma Importe"

	def CD_suma_asignado(self, obj):
		return obj.pago_set.all().aggregate(Sum('total_asignado'))['total_asignado__sum'] or 0
	def CH_suma_asignado(self, obj):
		return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_asignado(obj))
	CH_suma_asignado.allow_tags = True
	CH_suma_asignado.short_description = "Suma Asignado"
	
	def CD_suma_pendiente(self, obj):
		return obj.pago_set.all().aggregate(Sum('total_pendiente'))['total_pendiente__sum'] or 0
	def CH_suma_pendiente(self, obj):
		return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_pendiente(obj))
	CH_suma_pendiente.allow_tags = True
	CH_suma_pendiente.short_description = "Suma Pendiente"

	admin1_url = 'Admin1PlaNPago'
	
	admin1_url9 = 'Admin1PlaNPagoD'    
	def CH_admin1_url9(self, obj):
		href = "/%s/%s/?alias__startswith=%s" % (self.admin_site.name, self.admin1_url9.lower(), obj.alias)
		dev = u'<a href="%s">Entrar</a>' % href
		return dev
	CH_admin1_url9.allow_tags = True
	CH_admin1_url9.admin_order_field = 'tipodoc__alias'
	CH_admin1_url9.short_description = 'Ftras Pagadas'    

	def has_add_permission(self, request):
		return False
	def has_delete_permission(self, request, obj=None):
		return False


def def_Admin1PlaNPago():
	return {
		'campos': {
			'marca': {'etiq_form': 'Forma de Pago', 'etiq_list': 'Forma de Pago',
					  'definido': 'formaPago'},
			'bloqueado': {'etiq_form': 'Manual', 'etiq_list': 'Manual'},
			'fecha1': {'etiq_form': 'Fecha Pago', 'etiq_list': 'Fecha Pago'},
			'fecha2': {'etiq_form': 'Desde Fecha Venta', 'etiq_list': 'Desde Fecha Venta'},
			'fecha3': {'etiq_form': 'Hasta Fecha Venta', 'etiq_list': 'Hasta Fecha Venta'},
			'CC_fecha1': {'etiq_form': 'Fecha Pago', 'etiq_list': 'Fecha Pago'},

			'fecha2': {'etiq_form': 'Desde Fecha Venta', 'etiq_list': 'Desde Fecha Venta'},
			'fecha3': {'etiq_form': 'Hasta Fecha Venta', 'etiq_list': 'Hasta Fecha Venta'},
			'CC_fecha2': {'etiq_form': 'Desde Fecha Venta', 'etiq_list': 'Desde Fecha Venta'},
			'CC_fecha3': {'etiq_form': 'Hasta Fecha Venta', 'etiq_list': 'Hasta Fecha Venta'},
			'CC_fecha1_diasem': {'etiq_form': 'Dia Semana', 'etiq_list': 'Ds'},
			'total_asignado': {'etiq_form': 'Suma Ventas', 'etiq_list': 'Total Asignado'},
			'CD_suma_ventas':  {'etiq_form': 'Suma Ventas', 'etiq_list': 'Suma Ventas'},
			'CD_suma_ventas_libres':  {'etiq_form': 'Suma Ventas Libres', 'etiq_list': 'Suma Ventas Libres'},
			'CD_suma_ventas_otros':  {'etiq_form': 'Suma Ventas Otros', 'etiq_list': 'Suma Ventas Otros'},
		},
		'inlines': {
			'PagoDLIn': {
				'campos': {
					'cv': {'etiq_form': 'Factura', 'etiq_list': 'Factura'},
				},
			},
		}
	}


class PagoDLIn(TabularLIn):
	model = PagoD
	verbose_name_plural = "Facturas pagadas"
	fk_name = 'pago'
	fields = ('cv', 'importe', 'bloqueado')
	raw_id_fields = ('cv',)

class Admin1PlaNPago(Admin1TPD):
	model = Pago
	list_display = ('CC_fecha1', 'marca', 'importe', 'total_asignado',
					'total_pendiente', 'CC_fecha2', 'CC_fecha3',
					'CH_suma_ventas', 'CH_suma_ventas_libres', 'CH_suma_ventas_otros')
	fieldsets =  [
		(None, {
			'fields': [('marca', 'alias'),
				('fecha1', 'importe'),
				('fecha2', 'fecha3')]
			}),
		]
	readonly_fields = ('alias',)
	date_hierarchy = 'fecha1'
	ordering = ['alias']
	inlines = [PagoDLIn]
	
	def CD_suma_ventas(self, obj):
		cvs = CV.objects.filter(interno=False, 
						fecha1__gte=obj.fecha2, fecha1__lte=obj.fecha3)
		if cvs.count():
			return cvs.aggregate(Sum('total_facturar'))['total_facturar__sum']
		else:
			return 0
	CD_suma_ventas.short_description = "Suma Ventas"
	def CH_suma_ventas(self, obj):
		return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_ventas(obj))
	CH_suma_ventas.allow_tags = True
	CH_suma_ventas.short_description = "Suma Ventas"
	
	def CD_suma_ventas_libres(self, obj):
		cvs = CV.objects.filter(interno=False, marca='',
						fecha1__gte=obj.fecha2, fecha1__lte=obj.fecha3)
		if cvs.count():
			return cvs.aggregate(Sum('total_facturar'))['total_facturar__sum']
		else:
			return 0
	CD_suma_ventas_libres.short_description = "Ventas Contado"
	def CH_suma_ventas_libres(self, obj):
		return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_ventas_libres(obj))
	CH_suma_ventas_libres.allow_tags = True
	CH_suma_ventas_libres.short_description = "Ventas Contado"
	
	def CD_suma_ventas_otros(self, obj):
		return self.CD_suma_ventas(obj) - obj.total_asignado - self.CD_suma_ventas_libres(obj)
	CD_suma_ventas_otros.short_description = "Otras Tarjetas"
	def CH_suma_ventas_otros(self, obj):
		return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_ventas_otros(obj))
	CH_suma_ventas_otros.allow_tags = True
	CH_suma_ventas_otros.short_description = "Otras Tarjetas"

	def save_model(self, request, obj, form, change):
		f1 = obj.fecha1
		if f1:
			obj.tipodoc = get_crear_tipodoc('Pago', alias="%s" % f1.year) # , kwargs={})
			obj.alias = "%sT%sM%02dD%02d_%s" % (
						f1.year, obj.CE_fecha1_trimestre,
						f1.month, f1.day, obj.marca)
		return super(Admin1PlaNPago, self).save_model(request, obj, form, change)


def def_Admin1PlaNPagoD():
	return {
		'campos': {
			'marca':{'etiq_form': 'Forma de Pago', 'etiq_list': 'Forma de Pago'},
			'fecha1':{'etiq_form': 'Fecha Pago', 'etiq_list': 'Fecha Pago'},
		},
	}

class Admin1PlaNPagoD(Admin1Model):
	model = PagoD
	list_display = ['pago', 'marca', 'fecha1', 'CC_cv_orden','CC_cv_fecha1', 'importe']
	fieldsets =  [('datos', {'fields': ['alias']})]   
	date_hierarchy = 'fecha1'

	def CC_cv_orden(self, obj):
		return '' if not obj.cv else obj.cv.orden
	CC_cv_orden.admin_order_field = 'cv__orden'
	CC_cv_orden.short_description = 'Nº Factura'

	def CC_cv_fecha1(self, obj):
		if obj.cv.fecha1:
			return obj.cv.CC_fecha1
		else:
			return ''
	CC_cv_fecha1.admin_order_field = 'cv__fecha1'
	CC_cv_fecha1.short_description = 'Fecha Factura'		

	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False
	
	def change_view(self, request, object_id, form_url='', extra_context=None):
		return HttpResponseRedirect('../')

"""