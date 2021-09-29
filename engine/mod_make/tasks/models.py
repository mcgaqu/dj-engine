from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_admin.models.modeltree import ModelTree
from mod_auth.doctypes.models import ModelDocument



#--------------------------
# TASKS
#-----------------------------------
class Task(ModelDocument):
                           
    class Meta(ModelTree.Meta):
        verbose_name = _('Taarea')
        verbose_name_plural = _('1. Tareas')
        unique_together= (('doctype', 'alias'),)


class TaskAux(ModelAuxBase):
    trunk = models.ForeignKey(Task, on_delete=models.CASCADE, 
                                    related_name = "datax_set",
                                    null=True, blank=True)
    class Meta(ModelAuxBase.Meta):
        verbose_name = _('Detalle de Tarea')
        verbose_name_plural = _('2. Detalle de Tareas')
        unique_together= (('trunk','alias'),)
