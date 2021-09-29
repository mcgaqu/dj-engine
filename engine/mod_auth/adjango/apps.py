# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class AdjangoConfig(AppConfig):
    name = 'mod_auth.adjango'
    verbose_name = _('AUTHS: Adjango')
