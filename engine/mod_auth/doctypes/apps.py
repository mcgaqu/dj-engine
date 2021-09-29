# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _

class DocTypesConfig(AppConfig):
    name = 'mod_auth.doctypes'
    verbose_name = _(".2. Tipos de Documento")
