import decimal
from django.db.models import Sum
from mod_admin.utils.base import redondea
from mod_make.plans.models import Plan, PlanCV, PlanCVProduct, PlanCVTax


class PlanAdmin1Extra(object):
    pass
        # 'MU_Project', 'alias', 'locked', 'internal',
        # 'num_int', 
        #     'EE_sum_numftras_plan', 'EE_sum_cvs',
        # #-------------------
        # 'num_int1', 'num_dec1', 
        #     'ED_tax1', 'ED_total1',
        #         'ED_sum_base1_plan', 'ED_sum_base1_cvs', 
        #         'ED_sum_tax1_plan', 'ED_sum_tax1_cvs', 
        # 'num_int2', 'num_dec2',
        #     'ED_tax2', 'ED_total2',
        #         'ED_sum_base2_plan', 'ED_sum_base2_cvs',
        #         'ED_sum_tax2_plan', 'ED_sum_tax2_cvs',  
        # 'num_int3', 'num_dec3',
        #     'ED_tax3', 'ED_total3',             
        #         'ED_sum_base3_plan', 'ED_sum_base3_cvs',
        #         'ED_sum_tax3_plan', 'ED_sum_tax3_cvs', 
        # #----------------------------- 
        # 'ED_amount_base', 'ED_amount_tax', 'ED_amount_total'
        # 'ED_amount_base_plan', 'ED_amount_tax_plan', 'ED_amount_total_plan'
        # 'ED_amount_base_cvs', 'ED_amount_tax_cvs', 'ED_amount_total_cvs'
        # #----------------------------- 
        # 'num_dec', 'EB_ok3'
        #    'ED_sum_paid_plan', 'ED_sum_paid_cvs',
        # #------------------------------
        # 'EB_ok1' # num facturas plan == num ftras generadas
        # 'EB_ok2' # importe total plan == importe total facturas generadas
        # 'x_EB_0k3' # importe pago tarjeta plan < total ftras generadas
        # 'x_EB_ok4' # oke1 && ok2 && ok3
        # 'EB_ok_all'


class PlanAdmin1Extra(object):

#     EE_sum_numftras_plan', 'EE_sum_cvs',

    def EE_sum_numftras_plan(self, obj):
        plans = Plan.objects.filter(parent=obj)
        return 0 if not plans.count() else plans.aggregate(Sum('num_int'))['num_int__sum']

    def EE_sum_cvs(self, obj):
        cvs = PlanCV.objects.filter(alias__startswith=obj.alias)
        return 0 if not cvs.count() else cvs.count()


    def EC_cvs_ini_fin_sort(self, obj):
        cvs = PlanCV.objects.filter(alias__startswith=obj.alias).order_by('alias')
        if not cvs:
            return ''
        return "%s : %s" % (cvs[0].sort, cvs[cvs.count()-1].sort)
    EC_cvs_ini_fin_sort.short_description = "Rango Facturas"	

    def EC_cvs_ini_fin_alias(self, obj):
        cvs = PlanCV.objects.filter(alias__startswith=obj.alias).order_by('alias')
        if not cvs:
            return ''
        return "%s : %s" % (cvs[0].alias, cvs[cvs.count()-1].alias)
    EC_cvs_ini_fin_alias.short_description = "Rango Facturas (alias)"	


    #---------------------------------

    def ED_tax1(self, obj):
        if not obj.num_dec1:
            return 0
        return obj.num_dec1 * obj.num_int1/100
    def ED_total1(self, obj):
        if not obj.num_dec1:
            return self.ED_tax1(obj)
        return obj.num_dec1 + self.ED_tax1(obj)

    def ED_sum_base1_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        if not plans.count():
            return 0
        else:
            return redondea(plans.aggregate(Sum('num_dec1'))['num_dec1__sum'],2)
    
    def ED_sum_base1_cvs(self, obj): 
        cvtax = PlanCVTax.objects.filter(alias__startswith=obj.alias, porc_tax=obj.num_int1)
        if not cvtax.count():
            return 0
        else:
            return redondea(cvtax.aggregate(Sum('amount_base'))['amount_base__sum'],2)

    def ED_sum_tax1_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        if not plans.count():
            return 0
        else:
            dev = 0
            for plan in plans:
                dev += plan.num_dec1 + (plan.num_dec1 * plan.num_int1/100)
            return dev
    
    def ED_sum_tax1_cvs(self, obj): 
        cvtax = PlanCVTax.objects.filter(alias__startswith=obj.alias, porc_tax=obj.num_int1)
        return 0 if not cvtax.count() else cvtax.aggregate(Sum('amount_tax'))['amount_tax__sum']

    #--------------------------

    def ED_tax2(self, obj):
        return obj.num_dec2 * obj.num_int2/100
    def ED_total2(self, obj):
        return obj.num_dec2 + self.ED_tax2(obj)

    def ED_sum_base2_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        return 0 if not plans.count() else plans.aggregate(Sum('num_dec2'))['num_dec2__sum']
    
    def ED_sum_base2_cvs(self, obj): 
        cvtax = PlanCVTax.objects.filter(alias__startswith=obj.alias, porc_tax=obj.num_int2)
        return 0 if not cvtax.count() else cvtax.aggregate(Sum('amount_base'))['amount_base__sum']

    def ED_sum_tax2_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        if not plans.count():
            return 0
        else:
            dev = 0
            for plan in plans:
                dev += plan.num_dec2 + (plan.num_dec2 * plan.num_int2/100)
            return dev
    
    def ED_sum_tax2_cvs(self, obj): 
        cvtax = PlanCVTax.objects.filter(alias__startswith=obj.alias, porc_tax=obj.num_int2)
        return 0 if not cvtax.count() else cvtax.aggregate(Sum('amount_tax'))['amount_tax__sum']


    #-----------------------------------
    def ED_tax3(self, obj):
        return obj.num_dec3 * obj.num_int3/100
    def ED_total3(self, obj):
        return obj.num_dec3 + self.ED_tax3(obj)
        
    def ED_sum_base3_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        return 0 if not plans.count() else plans.aggregate(Sum('num_dec3'))['num_dec3__sum']
    
    def ED_sum_base3_cvs(self, obj): 
        cvtax = PlanCVTax.objects.filter(alias__startswith=obj.alias, porc_tax=obj.num_int3)
        return 0 if not cvtax.count() else cvtax.aggregate(Sum('amount_base'))['amount_base__sum']

    def ED_sum_tax3_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        if not plans.count():
            return 0
        else:
            dev = 0
            for plan in plans:
                dev += plan.num_dec3 + (plan.num_dec3 * plan.num_int3/100)
            return dev
    
    def ED_sum_tax3_cvs(self, obj): 
        cvtax = PlanCVTax.objects.filter(alias__startswith=obj.alias, porc_tax=obj.num_int3)
        return 0 if not cvtax.count() else cvtax.aggregate(Sum('amount_tax'))['amount_tax__sum']

    #-------------------------- 

    def ED_amount_base(self, obj):
        cero = decimal.Decimal(0.0)
        num_dec1 = cero if not obj.num_dec1 else obj.num_dec1
        num_dec2 = cero if not obj.num_dec2 else obj.num_dec3
        num_dec3 = cero if not obj.num_dec3 else obj.num_dec3
        return num_dec1 + num_dec2 + num_dec3
        # return self.ED_sum_basse1_plan(obj) + self.ED_sum_base2_plan(obj) + self.ED_sum_base3_plan(obj)
        # return self.ED_sum_base1_cvs(obj) + self.ED_sum_base2_cvs(obj) + self.ED_sum_base3_cvs(obj)

    def ED_amount_tax(self, obj):
        return self.ED_tax1(obj) + self.ED_tax2(obj) + self.ED_tax3(obj)

    def ED_amount_total(self, obj):
        return self.ED_amount_base(obj) + self.ED_amount_tax(obj)
    #------------------

    def ED_amount_base_cvs(self, obj):
        # return obj.num_dec1 + obj.num_dec2 + obj.num_dec3
        # return self.ED_sum_base1_plan(obj) + self.ED_sum_base2_plan(obj) + self.ED_sum_base3_plan(obj)
        return self.ED_sum_base1_cvs(obj) + self.ED_sum_base2_cvs(obj) + self.ED_sum_base3_cvs(obj)


    def ED_amount_tax_cvs(self,obj):
        # return self.ED_tax1 + self.ED_tax2 + self.ED_tax3
        # return self.ED_sum_tax1_plan(obj) + self.ED_sum_tax2_plan(obj) + self.ED_sum_tax3_plan(obj)
        return self.ED_sum_tax1_cvs(obj) + self.ED_sum_tax2_cvs(obj) + self.ED_sum_tax3_cvs(obj)
        
    def ED_amount_total_cvs(self,obj):
        # return self.ED_amount_base + self.ED_amount_tax
        return self.ED_amount_base_cvs(obj) + self.amount_tax_cvs(obj)

    #-----------------------------------
    # 'num_dec', 'EB_ok3'
        #    'ED_sum_paid_plan', 'ED_sum_paid_cvs',
    def ED_sum_paid_plan(self, obj): 
        plans = Plan.objects.filter(parent=obj)
        return 0 if not plans.count() else plans.aggregate(Sum('num_dec'))['num_dec__sum']

    def ED_sum_paid_cvs(self,obj):
        cvtax = PlanCV.objects.filter(alias__startswith=obj.alias)
        return 0 if not cvtax.count() else cvtax.aggregate(Sum('amount_paid'))['amount_paid__sum']

    #--------------------------------------------

    def EB_ok1(self, obj):
        """ Distinto nº de facturas previstas y Generadas
        o distinto importe venta previsto e Importe Facturaddo """
        # return (obj.entero1 != 0) and (obj.entero1-self.CE_num_cvs(obj)) == 0
        # return (obj.num_int != 0) and (obj.num_int-self.EE_sum_cvs(obj)) == 0
        return (obj.num_int-self.EE_sum_cvs(obj)) == 0
    EB_ok1.boolean = True
    EB_ok1.short_description = "Nº Ftras OK"

    def EB_ok2(self, obj):
        """ distinto base venta previsto e Bse Facturaddo """
        if obj.level == 3:
            return True
        return abs(self.ED_amount_base(obj)-self.ED_amount_base_cvs(obj)) < decimal.Decimal(0.1)
    EB_ok2.boolean = True
    EB_ok2.short_description = "Base OK"
    
    def x_EB_ok3(self, obj):
        """ Importe pagado por tarjeta < ventas del dia
        y todo asignado a facturas """
        c1 = self.CD_total_facturado(obj) >= self.CD_importe_pagado(obj)
        c2 = self.CD_importe_pagado(obj) == self.CD_importe_pago_asignado(obj)
        return c1 and c2
    x_EB_ok3.boolean = True
    x_EB_ok3.short_description = "Pagos OK"
    #---------------------------------
    
    def x_EB_ok4(self,obj):
        f0 = CV.objects.filter(alias__startswith=obj.alias,
                                 interno=False, total_base=0).count()
        return (f0 == 0)
    x_EB_ok4.boolean = True
    x_EB_ok4.short_description = "No Ftras 0"
    

    def EB_ok_all(self, obj):
        return self.EB_ok1(obj) and self.EB_ok2(obj) # and self.EB_ok3(obj) and self.EB_ok4(obj)
    EB_ok_all.boolean = True
    EB_ok_all.short_description = "Correct"


class PlanCVAdmin1Extra(object):
    pass



    #=======================================
"""
    def CD_total_base(self, obj):
        if not obj.total_base: # obj.nivel == 0:
            cvs = CV.objects.filter(alias__startswith=obj.alias,
                                interno=True, bloqueado=True)
            if cvs.count():
                return cvs.aggregate(
                        Sum('total_base'))['total_base__sum']
            else:
                return 0
        return obj.total_base
    def CH_total_base(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_total_base(obj))
    CH_total_base.allow_tags = True
    CH_total_base.short_description = "Total Base"
    
    def CD_total_facturar(self, obj):
        if not obj.total_facturar: # obj.nivel == 0:
            cvs = CV.objects.filter(alias__startswith=obj.alias,
                                # nivel = obj.nivel+1,
                                interno=True, bloqueado=True)
            if cvs.count():
                return cvs.aggregate(
                        Sum('total_facturar'))['total_facturar__sum']
            else:
                return 0
        return obj.total_facturar
    def CH_total_facturar(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_total_facturar(obj))
    CH_total_facturar.allow_tags = True
    CH_total_facturar.short_description = "Total Facturar"
    
    def CD_total_tasa(self, obj):
        return self.CD_total_facturar(obj) - self.CD_total_base(obj)
    def CH_total_tasa(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_total_tasa(obj))
    CH_total_tasa.allow_tags = True
    CH_total_tasa.short_description = "Total IVA"
    #---------------------------------	
    
    def CC_facturas_ini_fin(self, obj):
        ftras = CV.objects.filter(alias__startswith=obj.alias, interno=False).order_by(
            'fecha1','orden')
        if not ftras:
            return ''
        return "%s : %s" % (ftras[0].orden, ftras[ftras.count()-1].orden)
    CC_facturas_ini_fin.short_description = "Rango Facturas"	

    def CC_facturas_ini_fin_alias(self, obj):
        ftras = CV.objects.filter(alias__startswith=obj.alias, interno=False).order_by(
            'fecha1','alias')
        if not ftras:
            return ''
        return "%s : %s" % (ftras[0].alias, ftras[ftras.count()-1].alias)
    CC_facturas_ini_fin_alias.short_description = "Rango Facturas (alias)"	
    #---------------------------------
    def CE_num_cvs(self, obj):
        return CV.objects.filter(alias__startswith=obj.alias,
                                 interno=False).count()
    CE_num_cvs.short_description = 'Nº Ftras'
    
    def CE_num_cvps(self, obj):
        if obj.interno == False:
            return obj.CE_num_cvps()
        if obj.nivel == 3:
            return CVProducto.objects.filter(
                cv__fecha1=obj.fecha1, cv__interno=False).count()
        else:
            conta = 0
            for h in obj.hijos.all():
                conta += self.CE_num_cvps(h)
            return conta
    CE_num_cvps.short_description = 'Nº Líneas'	
    #------------------------
 
    def CD_total_facturado(self, obj):
        cvs = CV.objects.filter(alias__startswith=obj.alias,
                                interno=False)
        if cvs.count():
            return cvs.aggregate(
                    Sum('total_facturar'))['total_facturar__sum']
        else:
            return 0
    def CH_total_facturado(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_total_facturado(obj))
    CH_total_facturado.allow_tags = True
    CH_total_facturado.short_description = "Facturado"    
    
    #-------------------------------------
    def CE_num_pagos(self, obj):
        return Pago.objects.filter(alias__startswith=obj.alias).count()
    CE_num_pagos.short_description = "Nº Pagos"   

    def CE_num_pagod(self, obj):
        return PagoD.objects.filter(cv__alias__startswith=obj.alias).count()
    CE_num_pagod.short_description = "Nº Ftras Pagadas"

    def CD_importe_pagado(self, obj):
        pagos = Pago.objects.filter(alias__startswith=obj.alias)
        if pagos.count():
            return pagos.aggregate(
                Sum('importe'))['importe__sum']
        else:
            return 0
    CD_importe_pagado.short_description = 'Suma Pagos'
    def CH_importe_pagado(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_importe_pagado(obj))
    CH_importe_pagado.allow_tags = True
    CH_importe_pagado.short_description = "Suma Pagos"        
    
    def CD_importe_pago_asignado(self, obj):
        pagos = Pago.objects.filter(alias__startswith=obj.alias)
        if pagos.count():
            return pagos.aggregate(
                Sum('importe'))['importe__sum']
        else:
            return 0
    CD_importe_pago_asignado.short_description = 'Suma Pagos Asignados'
    def CH_importe_pago_asignado(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_importe_pago_asignado(obj))
    CH_importe_pago_asignado.allow_tags = True
    CH_importe_pago_asignado.short_description = "Suma Pagos Asignados"        

    def CD_suma_facturas_pagadas(self, obj):
        pagods = PagoD.objects.filter(cv__alias__startswith=obj.alias)
        if pagods.count():
            return pagods.aggregate(
                Sum('importe'))['importe__sum']
        else:
            return 0
    CD_suma_facturas_pagadas.short_description = 'Suma Ftras Pagadas'
    def CH_suma_facturas_pagadas(self, obj):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_suma_facturas_pagadas(obj))
    CH_suma_facturas_pagadas.allow_tags = True
    CH_suma_facturas_pagadas.short_description = 'Suma Ftras Pagadas'   
    
    def CD_porc_pago(self, obj):
        if obj.total_facturar == 0:
            return 0
        else:
            return redondea(self.CD_importe_pagado(obj)/obj.total_facturar*100,2)
    CD_porc_pago.short_description = '% Pago'
"""