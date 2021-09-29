# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class CommandsConfig(AppConfig):
    name = 'mod_order.commands'
    verbose_name = _("41. GESTION: Pedidos")
