# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'mod_entity.projects'
    verbose_name = _("23. ENTIDADES: Proyectos")
