
import decimal
from django.db import models
from django.conf import settings

from django.utils.translation import gettext, gettext_lazy as _
from django.db.models.query import prefetch_related_objects
from django.utils.html import format_html

# from django.utils.timezone import activate

from mod_admin.models.modelbase import ModelBase # , ModelAuxBase
# from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument

from mod_auth.companies.models import Company
from mod_entity.persons.models import Person
from mod_entity.products.models import Product
from mod_entity.projects.models import Project, ProjectAux

# from mod_order.payments.models import Payment



class Plan(ModelDocument):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, 
                                    # limit_choices_to={'doctype__alias':'PLAN'},
                                    null=True, blank=True)
    patron_alias = models.CharField(max_length=150, null=True, blank=True)

    plan_year_id = models.IntegerField(null=True, blank=True)

    num_int1 = models.IntegerField(default=0)
    num_dec1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    num_int2 = models.IntegerField(default=0)
    num_dec2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    num_int3 = models.IntegerField(default=0)
    num_dec3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)



    def MU_Project(self):
        # TODO! para Bases de datos multisitio
        # href = "/%s/auth/user/?biz__id=%s" % (settings.SITE_NAME, self.id)
        href = "/%s/projects/project/%s/change/" % (settings.SITE_NAME, self.project.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.project.alias)


    class Meta(ModelDocument.Meta):
        verbose_name = _('Plan')
        verbose_name_plural = _('1. Plans')
        unique_together= (('project', 'alias'),)


class PlanCV(ModelDocument):

    #--------------------------------
    # date1 = fecha factura
    # date2 = fecha pago
    # grade = trimestre de date1
    # alias = código interno
    # sort = Nº de factura externo (oficial)
    # note1
    # note2
    #-------------------------
    project = models.ForeignKey(Project, on_delete=models.CASCADE, 
                                    # limit_choices_to={'doctype__alias':'PLAN'},
                                    null=True, blank=True)
    
    sign = models.IntegerField(choices=(
        (1, 'Entrada',), (-1, 'Salida'), (0, 'Traspaso')), null=True, blank=True)

    #-------------------
    tercero = models.ForeignKey(Person, on_delete=models.PROTECT,
                                # related_name = "%(class)s_tercero",
                                null=True, blank=True)
    #-------------------
   
    #------------------------------------------------
    amount_base =  models.DecimalField(max_digits=15, decimal_places=4,
                                        default=0, null=True, blank=True)
    amount_tax =  models.DecimalField(max_digits=15, decimal_places=4,
                                       default=0, null=True, blank=True)

    amount_total = models.DecimalField(max_digits=15, decimal_places=4,
                                        default=0, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=4,
                                        default=0, null=True, blank=True)

    #-------------------------------------------
    
    class Meta(ModelDocument.Meta):
        verbose_name = "Invoice"
        verbose_name_plural = "3. Invoices"

    
    def __str__(self):
        return "%s-%s" % (self.doctype.alias, self.alias)


    def CE_num_cvps(self):
        return self.plancvproduct_set.all().count()
    CE_num_cvps.short_description = "Nº líneas"
    
    # def CC_date1_periodo(self):
    #     if not self.date1:
    #         xx = {0:'0000', 1:'0000T0', 2:'0000T0M00', 3:'0000T0M00D00'}
    #     else:
    #         xx = {
    #             0:"%s" % self.date1.year,
    #             1:"%sT%s" %  (self.date1.year, self.CE_date1_trimestre),
    #             2:"%sT%sM%02d" % (self.date1.year, self.CE_date1_trimestre,
    #                             self.date1.month),
    #             3:"%sT%sM%02dD%02d" % (self.date1.year, self.CE_date1_trimestre,
    #                             self.date1.month, self.date1.day),
    #         }
    #     return xx[self.nivel]

    
    @property
    def LR_lines_product(self):
        res = []
        if self.id:
            res = list(self.plancvproduct_set.all())
            return res
        return res

    @property
    def LR_lines_tax(self):
        res = []
        if self.id:
            res = list(self.plancvtax_set.all())
            return res
        return res

    @property
    def CD_amount_base(self):
        total = 0   
        for lin in self.LR_lines_product:
            total += lin.CD_price_base * lin.units
        return total
    
    #----------
    def CH_amount_base(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_base)
    CH_amount_base.allow_tags = True
    CH_amount_base.short_description = "Total Base" 

    def CH_amount_tax(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.amount_tax)
    CH_amount_tax.allow_tags = True
    CH_amount_tax.short_description = "Total IVA"       

    def CH_amount_total(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.amount_total)
    CH_amount_total.allow_tags = True
    CH_amount_total.short_description = "Total Facturar"    

    def CH_amount_paid(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.amount_paid)
    CH_amount_paid.allow_tags = True
    CH_amount_paid.short_description = "Total Pagado"    

    def CD_amount_pdte(self):
        return self.ammount_total - self.amount_paid
    CD_amount_pdte.short_description = "Pendiente Pago"    
    def CH_amount_pdte(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_pdte())
    CH_amount_pdte.allow_tags = True
    CH_amount_pdte.short_description = "Pendiente Pago"  



    @property
    def CD_amount_tax(self):
        total = 0   
        for lin in self.LR_lines_tax:
            total += lin.CD_amount_tax
        return total
        # return redondea(total,4)
    
    def CH_amount_tax(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_tax)
    CH_amount_tax.allow_tags = True
    CH_amount_tax.short_description = "Total IVA"    


    # @property
    # def CD_amount_iva(self):
    #     total = 0   
    #     for lin in self.LR_lineas_producto:
    #         total += lin.unidades * lin.CD_precio_base * lin.CD_porc_iva/100
    #     return total


    @property    
    def DL_lines_tax(self):
        lines = {}
        for l in self.LR_lines_product:
            # clave = (l.tasa, l.producto_pc)
            clave = l.porc_tax
            if not clave in lines.keys():
                clave = l.porc_tax
                lines[clave] =  l.amount_base
            else:
                lines[clave] += l.amount_base
        return lines   
 

    def save_tax(self):
        # import pdb; pdb.set_trace()
        self.plancvtax_set.all().update(active=False)
        for clave, base in self.DL_lines_tax.items():
            try:
                limp = PlanCVTax.objects.get(alias=self.alias,
                            cv=self, porc_tax=clave)
            except PlanCVTax.DoesNotExist:
                limp = PlanCVTax(alias=self.alias,
                            cv=self, porc_tax=clave)
            
            limp.amount_base = base
            limp.amount_tax = base * clave / decimal.Decimal(100)
            limp.active=True
            #------------------------------
            # guardar campos de cv para facilitar pantallas de ivas
            #------------------------
            limp.date1 = self.date1
            limp.sort = self.sort # Número de factura
            # limp.num_int = self.plan.id
            limp.grade = self.grade # trimestre aaaaTx
            #--------------------------
            limp.save()
        self.plancvtax_set.filter(active=False).delete()

 

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # self.grade =  self.plan.grade # "%sT%s" %  (self.date1.year, self.CE_date1_trimestre)
        self.amount_base = self.CD_amount_base
        self.amount_tax = self.CD_amount_tax
        self.amount_total = self.amount_base + self.CD_amount_tax 
        super().save(*args, **kwargs)
        # self.save_tasa()

    def regrabar(self):
        self.save()
        self.save_tax()




class PlanCVProduct(ModelBase):


    cv = models.ForeignKey(PlanCV, on_delete=models.PROTECT)
 
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                 null=True, blank=True)
 
    units = models.DecimalField(max_digits=15,
                                            decimal_places=4,
                                            default=1, null=True, blank=True)
    price = models.DecimalField(max_digits=15,
                                            decimal_places=4,
                                            default=0, null=True, blank=True)

    tax_included = models.BooleanField(default=False)
    porc_tax = models.DecimalField(max_digits=5, decimal_places=0, default=0,
                                    null=True, blank=True)
    
    # tax = models.ForeignKey(PlanFactorAux, on_delete=models.PROTECT)
    #------------------------    
    amount_base = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       null=True, blank=True)
    amount_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       null=True, blank=True)
    amount_total = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       null=True, blank=True)

    
    class Meta(ModelBase.Meta):
        # unique_together = (('cv', 'alias'),)    
        verbose_name = 'PlanDoc Producto'
        verbose_name_plural = '3.1 PlanDoc Productos'
        # ordering = ['lin']

    def __str__(self):
        return "%s_%s" % (
            #self.cv.alias, self.product.alias)
            self.cv.alias, self.id)



    def CF_cv_date1(self):
        if self.cv.date1:
            return self.cv.date1
        else:
            return None
    CF_cv_date1.short_description = 'Fecha Ftra.'
    CF_cv_date1 = property(CF_cv_date1)
    
    def CC_cv_sort(self):
        return self.cv.sort
    CC_cv_sort.short_description = 'Número Ftra.'
    CC_cv_sort.admin_order_field = 'cv__sort'   
    
    def CC_cv_grade(self):
        return self.cv.sort
    CC_cv_grade.short_description = 'grupo'
    CC_cv_grade.admin_order_field = 'cv__grade'   
    
    def CC_cv_alias(self):
        return self.cv.alias
    CC_cv_alias.short_description = 'Código Ftra.'
    CC_cv_alias.admin_order_field = 'cv__alias'


    def CH_porc_tax(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.porc_tax)
    CH_porc_tax.allow_tags = True
    CH_porc_tax.short_description = '% IVA'           
    
        
    @property
    def CD_price_base(self):
        # precio base: sin iva con descuento 
        if not self.tax_included:
            return self.price
        else:
            return self.price/(1+self.porc_tax/100)

    @property
    def CD_amount_base(self):
        return self.units * self.CD_price_base
    def CH_amount_base(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_base)
    CH_amount_base.allow_tags = True
    CH_amount_base.short_description = 'Importe Base'

    @property
    def CD_amount_tax(self):
        return self.units * self.CD_price_base * self.porc_tax/100
    def CH_amount_tax(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_tax)
    CH_amount_tax.allow_tags = True
    CH_amount_tax.short_description = 'Importe IVA'
    
    @property
    def CD_amount_total(self):
        return self.CD_amount_base + self.CD_amount_tax
    def CH_amount_total(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_tax)
    CH_amount_total.allow_tags = True
    CH_amount_total.short_description = 'Importe Total'
    

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # self.alias = self.cv.alias
        self.date1 = self.cv.date1
        self.grade = self.cv.grade
        self.sort = self.cv.sort
        self.amount_base = self.CD_amount_base
        self.amount_tax = self.CD_amount_tax
        self.amount_total = self.CD_amount_total
        super().save(*args, **kwargs)



class PlanCVTax(ModelBase):

    cv = models.ForeignKey(PlanCV,
                           on_delete=models.CASCADE,
                           null=True, blank=True)

    porc_tax = models.DecimalField(max_digits=5, decimal_places=0, default=0,
                                    null=True, blank=True)
    amount_base = models.DecimalField(max_digits=15, decimal_places=2, default=0)        

    amount_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                    null=True, blank=True)


    class Meta(ModelBase.Meta):
        verbose_name = "CV Tax"
        verbose_name_plural = "CV Taxs"
        unique_together = [('cv', 'alias', 'porc_tax')]
       
    
    def CH_porc_tax(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.porc_tax)
    CH_porc_tax.allow_tags = True
    CH_porc_tax.short_description = '% IVA'
    
    def CD_amount_tax(self):
        return self.porc_tax/100 * self.amount_base
    CD_amount_tax.short_description = 'amount Tax'
    CD_amount_tax = property(CD_amount_tax)
    
    def CH_amount_tax(self):
        return '<span class="Totales">%s</span>' % '{:,.2f}'.format(self.CD_amount_tax)
    CH_amount_tax.allow_tags = True
    CH_amount_tax.short_description = 'amount Tax'    

    #def CF_cv_date1(self):
    #    if self.cv.date1:
    #        return self.cv.date1
    #    else:
    #        return None
    #CF_cv_date1.short_description = 'Fecha Ftra.'
    #CF_cv_date1 = property(CF_cv_date1)
    #
    #def CC_cv_sort(self):
    #    return self.cv.sort
    #CC_cv_sort.short_description = 'Número Ftra.'
    #CC_cv_sort.admin_order_field = 'sort'   
    #
    #def CC_cv_alias(self):
    #    return self.cv.alias
    #CC_cv_alias.short_description = 'Código Ftra.'

    def __str__(self):
        return "%s_%s" % (self.cv.alias, self.porc_tax)

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        self.alias = self.cv.alias
        self.date1 = self.cv.date1
        self.grade = self.cv.grade
        self.sort = self.cv.sort
        # self.entero = self.cv.tipodoc.id
        super().save(*args, **kwargs)

