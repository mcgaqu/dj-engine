# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class InvoicesConfig(AppConfig):
    name = 'mod_order.invoices'
    verbose_name = _("42. GESTION: Facturas")
