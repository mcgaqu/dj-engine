# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class TasksConfig(AppConfig):
    name = 'mod_make.tasks'
    verbose_name = _("32. PRODUCCION: Tareas")
