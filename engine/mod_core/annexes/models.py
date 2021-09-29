from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from mod_admin.models.modelbase import ModelBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument




#--------------------------
# Archivo Anexo
#-----------------------------------
class Folder(ModelDocument):

    docfile = models.FileField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)

    class Meta(ModelTree.Meta):
        verbose_name = _('Carpetas')
        verbose_name_plural = _('1. Carpetas: SubCarpetas y documentos')
        unique_together= (('doctype', 'alias'),)
        ordering = ('sort', 'grade')

    def __str__(self):
        if not self.docfile:
            return "Folder: %s" % self.alias
        else:
            return "Doc: %s" % self.alias

    def MH_content(self):
        if not self.content:
            return ""
        return format_html(self.content)

class FolderAnnex(ModelBase):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    ctt = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                            null=True, blank=True)
    obj_id = models.PositiveIntegerField(null=True, blank=True)
    ctt_obj = GenericForeignKey('ctt', 'obj_id')


    class Meta(ModelBase.Meta):
        verbose_name = _('Anexo')
        verbose_name_plural = _('2. Anexos')
        unique_together= (('folder','ctt', 'obj_id', 'alias'),)
