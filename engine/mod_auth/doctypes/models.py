
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.html import format_html
from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.companies.models import Company


#--------------------------
# DocType
#-----------------------------------
class DocType(ModelTree):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    # bmodel = models.ForeignKey(BModel, on_delete=models.CASCADE, 
    #                                 null=True, blank=True)      
    model_name = models.CharField(max_length=250, null=True, blank=True) 

    # grade = patron_alias = models.CharField(max_length=150, null=True, blank=True)

    def ME_num_folders(self):
        
        return self.folder_set.count()
    ME_num_folders.short_description = _("Nº Folders")

    def MU_Folder(self):
        href = "/%s/annexes/folder/?doctype__id=%s" % (settings.SITE_NAME, self.id)
        return format_html('<a href="{}">({}) IR</a>', href, self.ME_num_folders())
    MU_Folder.short_description = _("Folders") 
 

    class Meta(ModelTree.Meta):
        verbose_name = _('Tipo de Documento')
        verbose_name_plural = _('1. Tipos de Documentos')
        unique_together= (('company', 'model_name', 'alias'),)

# def x_get_create_doctype(modelo, alias=None, **kwargs):
#     tabla = Tabla.objects.get(alias=modelo)
#     alias = alias or modelo
#     params = kwargs.get('kwargs', None)
#     # import pdb; pdb.set_trace()
#     try:
#         td = TipoDoc.objects.get(tabla=tabla, alias=alias)
#     except TipoDoc.DoesNotExist:
#         td = TipoDoc(tabla=tabla, alias=alias)
#     td.nombre = "%s_%s" % (tabla.alias, alias)
#     if params:
#         for k,valor in six.iteritems(params):
#             setattr(td, k, valor)
#         if not td.empresa:
#             empresa = Empresa.objects.get(alias=settings.INSTAL)
#             td.empresa = empresa
#     td.save()
#     return td

class DocTypeProp(ModelBase):
    doctype = models.ForeignKey(DocType, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    class Meta(ModelBase.Meta):
        verbose_name = _('Propiedad de TPD')
        verbose_name_plural = _('2. Propiedades de TPD')
        unique_together= (('doctype','alias'),)


def get_create_doctype(company, alias_model):
    try:
        dt = DocType.objects.get(model_name=alias_model, company=company, alias=alias_model)
    except DocType.DoesNotExist:
        dt = DocType(model_name=alias_model, company=company, alias=alias_model)
        dt.name = alias_model
        dt.save()
    return dt



class ModelDocument(ModelTree):
    doctype = models.ForeignKey(DocType, on_delete=models.CASCADE, 
                                    null=True, blank=True)

    date1 = models.DateField(null=True, blank=True)
    datet1 = models.DateField(null=True, blank=True)
    date2 = models.DateField(null=True, blank=True)
    datet2 = models.DateField(null=True, blank=True)
    note1 = models.TextField(null=True, blank=True)
    note2 = models.TextField(null=True, blank=True)


    def MC_date1(self):
        if self.date1:
            return self.date1.strftime('%d/%m/%Y')
        else:
            return ''
    MC_date1.admin_order_field = 'date1'
    MC_date1.short_description = 'date 1'
    MC_date1 = property(MC_date1)
    
    def MC_date1_diasem(self):
        diasem = {0:'L', 1:'M', 2:'X', 3:'J', 4:'V', 5:'S', 6:'D'}
        if not self.date1: #  or self.nivel < 3:
            return ''
        else:
            return diasem[self.date1.weekday()]
    MC_date1_diasem.short_description = 'Dia Semana'
    MC_date1_diasem = property(MC_date1_diasem)
    
    @property
    def ME_date1_trimestre(self):
        if not self.date1:
            return 0
        if self.date1.month % 3 > 0:
            return self.date1.month/3 +1
        else:
            return self.date1.month/3
    
    def MC_date1_periodo(self):
        xx = {
            0:"%s" % self.date1.year,
            1:"%sT%s" %  (self.date1.year, self.CE_date1_trimestre),
            2:"%sT%sM%02d" % (self.date1.year, self.CE_date1_trimestre,
                            self.date1.month),
            3:"%sT%sM%02dD%02d" % (self.date1.year, self.CE_date1_trimestre,
                            self.date1.month, self.date1.day),
        }
        return xx[self.nivel]

    #-------------------------------







    def get_create_doctype(self, model_name, company_id=settings.COMPANY_ID, 
                            alias=None, **kwargs):
        company = Company.objects.get(id=company_id)
        alias = alias or model_name
        params = kwargs.get('kwargs', None)
        # import pdb; pdb.set_trace()
        try:
            dt = DocType.objects.get(model_name=model_name, company=company, alias=alias)
        except DocType.DoesNotExist:
            dt = DocType(model_name=model_name, company=company, alias=alias)
            if params:
                for k,valor in params.items():
                    setattr(dt, k, valor)
            dt.save()
        return dt

    def save(self, *args, **kwargs):
        if not hasattr(self, 'doctype') or not self.doctype:
            if not self.parent:
                self.doctype = self.get_create_doctype(
                    self.__class__.__name__)
            else:
                self.doctype = self.parent.doctype
        return super().save(*args, **kwargs)

    class Meta(ModelTree.Meta):
        abstract = True
        unique_together= (('doctype','alias'),)


