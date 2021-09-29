# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class PersonsConfig(AppConfig):
    name = 'mod_entity.persons'
    verbose_name = _("21. ENTIDADES: Personas")
