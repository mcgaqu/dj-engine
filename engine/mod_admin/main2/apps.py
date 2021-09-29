# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class Main2Config(AppConfig):
    name = 'mod_admin.main2'
    verbose_name = _('ADMIN: Main2')
