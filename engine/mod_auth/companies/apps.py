# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _

class CompaniesConfig(AppConfig):
    name = 'mod_auth.companies'
    verbose_name = _('.1. Empresas')
