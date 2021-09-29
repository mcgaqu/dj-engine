# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class PaymentsConfig(AppConfig):
    name = 'mod_order.payments'
    verbose_name = _("42. GESTION: FacturasPagos")
