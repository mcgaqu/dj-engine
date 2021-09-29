
from .actions1 import ac_create_projects, ac_import_planyear						
from .actions2 import ac_create_planyear
from .actions3 import ac_generate_planyear
from .actions4 import ac_generate_plancvs, ac_renumerar_cvs
from .actions5 import ac_export_planreport_pdf, ac_export_planreport_xls
# from .actions6 import ac_PlanCVpdf, ac_PlanCVxls				


def get_app_actions(index):
    dev = {
		'Company': [
			ac_create_projects, # un proyecto "limpio" por hoja/year del fichero Company.xls
		],
		'Project':[
			ac_import_planyear, # los datos-factor de la hoja de calculo
			ac_create_planyear, # un registro "limpio" por cada T/M/D del año 
								# + actualizar datos de Venta de projectaux y bloqueando	

		],
		'Plan': [
			ac_generate_planyear, # calcular descendientes hasta dia:
					# 1- respetando los bloqueados
					# 2- aplicando pesos globales por rango fechas y (periodos/diasem): de num-ftras e importe venta
					# 3- modificando aleatoriamente para que no salgan iguales
			ac_generate_plancvs, # generar facturas a partir de dia:
				# 'ac_generar_cvs', 
				# 'ac_generar_cvproductos',
			ac_renumerar_cvs,
				# 'ac_cv_ajustar_tarjeta',
				'ac_revisar_datos',	

			ac_export_planreport_pdf,
			ac_export_planreport_xls,

		],
		#-----------
		'PlanCV': [
			'ac_PlanCVpdf', 
			'ac_PlanCVxls'
		],
		'Payment': [],
		# -----
    }
    return dev[index]


"""
from .actions.actions1 import (# get_prioridad,
								ac_tdcv_crear_ejercicios,
								ac_tdcv_importar_ejercicio,
								ac_tdcv_importar_tarifa,
								ac_tdcv_importar_ventas,
								ac_tdcv_importar_pagos,
								ac_tdcv_importar_factores,
								ac_tdcv_eliminar_ejercicios,
								)

from .actions.actions2 import ac_calcular_dias

from .actions.actions3 import ( ac_generar_cvs, ac_generar_cvproductos,
							    ac_renumerar_facturas,
								ac_cv_ajustar_tarjeta,
								#--------------------
								# ac_tdpago_calcular_fechas_venta,
								#ac_tdpago_ajustar_tarjeta,
								#ac_tdpago_desajustar_tarjeta,
								#ac_pago_calcular_fechas_venta,
								#ac_pago_ajustar_tarjeta,
								#ac_pago_desajustar_tarjeta,
								#---------------
								ac_revisar_datos							   
								)

from .actions.actions4 import ac_CVpdf, ac_CVxls
from .actions.actions4 import ac_cv1_informes, ac_cv1_informe_resumen # ac_tdcv_informes

"""


