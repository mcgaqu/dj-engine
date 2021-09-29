# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, linebreaks
from django.utils.translation import gettext, gettext_lazy as _

class ModelBase(models.Model):

    alias = models.CharField(verbose_name=_('código'), max_length=100, null=True, blank=True)
    name = models.CharField(verbose_name=_('nombre'), max_length=200, null=True, blank=True)
    grade = models.CharField(verbose_name=_('clase'), max_length=50, null=True, blank=True)
    sort = models.CharField(verbose_name=_('orden'), max_length=20, null=True, blank=True)

    active = models.BooleanField(verbose_name=_('activo'), default=True)
    internal = models.BooleanField(verbose_name=_('interno'), default=False)
    locked = models.BooleanField(verbose_name=_('bloqueado'), default=False)
    replace = models.BooleanField(verbose_name=_('reemplaza'), default=False)

    datet = models.DateTimeField(verbose_name=_('fecha-hora'), default=timezone.now, null=True, blank=True)
    date = models.DateField(verbose_name=_('fecha'), default=timezone.now, null=True, blank=True)
    num_int = models.IntegerField(default=0)
    num_dec = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    mark = models.CharField(max_length=250, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    note = models.TextField(verbose_name=_('nota'), null=True, blank=True)    
    json = models.JSONField(verbose_name=_('valor'),null=True, blank=True)

    file = models.FileField(verbose_name=_('file'), null=True, blank=True)
    # estado = JSONField(null=True, blank=True)


    class Meta():
        abstract = True
        ordering = ['sort']
        # default_permissions = []
        
    def __str__(self):
        return "%s" % self.alias
        # return "%s - %s" % (self.alias, self.name)

    def MC_sort_alias(self):
        sort = self.sort or ""
        alias = self.alias or ""
        return "%s%s" % (sort, alias)
    MC_sort_alias.short_description = "Sort-Alias"

    def MC_grade_sort(self):
        sort = self.sort or ""
        grade = self.grade or ""
        return "%s%s" % (grade,sort)
    MC_grade_sort.short_description = "Grade-Sort"

    def MC_indent_alias(self):
        if not self.grade:
            return self.alias
        return "%s %s" % ("__"*(len(self.grade)-1), self.alias)
    MC_indent_alias.short_description = "Alias"

    def MC_name_note(self):
        return format_html("<span>{}</span></br>{}",self.name.upper(),self.note)

    #-------------------------
    def MC_date(self):
        if self.date:
            return self.date.strftime('%d/%m/%Y')
        else:
            return ''
    MC_date.admin_order_field = 'date'
    MC_date.short_description = 'date'
    MC_date = property(MC_date)

    MC_name_note.short_description = "Description"

    def MC_date_diasem(self):
        diasem = {0:'L', 1:'M', 2:'X', 3:'J', 4:'V', 5:'S', 6:'D'}
        if not self.date: #  or self.nivel < 3:
            return ''
        else:
            return diasem[self.date.weekday()]
    MC_date_diasem.short_description = 'Dia Semana'
    MC_date_diasem = property(MC_date_diasem)
    
    @property
    def ME_date_trimestre(self):
        if not self.date:
            return 0
        if self.date.month % 3 > 0:
            return int(self.date.month/3) +1
        else:
            return int(self.date.month/3)
    
    def MC_date_periodo(self):
        xx = {
            0:"%s" % self.date.year,
            1:"%sT%s" %  (self.date.year, self.ME_date_trimestre),
            2:"%sT%sM%02d" % (self.date.year, self.ME_date_trimestre,
                            self.date.month),
            3:"%sT%sM%02dD%02d" % (self.date.year, self.ME_date_trimestre,
                            self.date.month, self.date.day),
        }
        return xx[self.nivel]

class ModelAuxBase(ModelBase):
    # trunk = models.ForeignKey(ModelBase, on_delete=models.CASCADE, 
    #                                 related_name = "datax_set",
    #                                 null=True, blank=True)
    inline = models.CharField(verbose_name=_('pestaña'), max_length=50, null=True, blank=True)
    line = models.CharField(verbose_name=_('linea'), max_length=20, null=True, blank=True)
    valuex = models.JSONField(null=True, blank=True) 

    class Meta(ModelBase.Meta):
        abstract = True 
        unique_together = (('trunk', 'inline', 'line', 'alias'))

    def __str__(self):
        return ""
    
    def x_MJ_valuex(self):
        return self.valuex