# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class Main1Config(AppConfig):
    name = 'mod_admin.main1'
    verbose_name = _('ADMIN: Main1')
