# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


class ModelAdmin1(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

class ModelAuxAdmin1(ModelAdmin1):
    pass


class ModelLin1(admin.TabularInline):
    extra = 0
    classes = ['collapse']

class ModelAuxLin1(ModelLin1):
    fields = ['grade', 'sort', 'alias','valuex']
    fk_name = 'trunk'
    tab_label = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.tab_label:
            qs = qs.filter(inline=self.tab_label)    
        return qs

class GenericLin1(GenericTabularInline):
    wiew_on_site = False
    extra = 0

    ct_field = 'ctt_field'
    ct_fk_field = 'obj_id'

    template = 'admin/edit_inline/tabular.html'

"""

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'other'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

   
    class MultiDBTabularInline(admin.TabularInline):
        using = 'other'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
"""