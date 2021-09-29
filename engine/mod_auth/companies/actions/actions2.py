# -*- coding: utf-8 -*-
import os, sys
from importlib import import_module
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _



def ac_import_data(modeladmin, request, queryset):
    """
        1. Ejecutar la función definida en cada registro 
    """

    for obj in queryset:
        # import pdb; pdb.set_trace()
        if not obj.locked:
            mod_import = import_module('%s' % obj.grade)
            func_import = getattr(mod_import, obj.alias)
            func_import(modeladmin, request, obj)
            message = "Función %s realizada" % obj.alias
        else:
            message = _("el id:%s, %s no se carga porque está bloqueado") % (obj.id, obj.name)
        modeladmin.message_user(request, message, level=messages.SUCCESS)
    return
ac_import_data.short_description = "Importar Datos"


def base_load(modeladmin, request, queryset, obj=None):
    """
        Importar fichero: modelo_origen, modelo_destino
    """


    mensaje = "Importación de datos"
    return (mensaje, messages.SUCCESS)
