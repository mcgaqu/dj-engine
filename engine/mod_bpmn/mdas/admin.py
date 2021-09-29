from django.conf import settings
from django.contrib import admin
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
from .models import Mda, MdaView, MdaViewAux, MdaAux


class MdaViewAuxAdmin1(ModelAuxAdmin1):
    model = MdaViewAux
    list_display = ['mdaviewc', 'alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']


class MdaViewAuxLin1(ModelAuxLin1):
    model = MdaViewAux
    fk_name = 'mdaviewc'
    fields = ['alias', 'name', 'grade', 'sort']


class MdaViewAdmin1(ModelAdmin1):
    model = MdaView
    list_display = ['mda', 'alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    list_filter = ['mda__biz', 'mda']
    inlines = [MdaViewAuxLin1]


class MdaAuxAdmin1(ModelAuxAdmin1):
    model = MdaAux
    list_display = ['mda', 'alias', 'name', 'grade', 'sort']
    fields = ['alias', 'name', 'grade', 'sort']
    list_filter = ['mda__biz', 'mda']

class MdaAuxLin1(ModelAuxLin1):
    model = MdaAux
    fk_name = 'mda'
    fields = ['alias', 'name', 'grade', 'sort']


class MdaViewLin1(ModelLin1):
    model = MdaView
    fk_name = 'mda'
    fields = ['alias', 'name', 'grade', 'sort']


class MdaAdmin1(ModelAdmin1):
    model = Mda
    inlines = [MdaAuxLin1, MdaViewLin1]
    list_display = ['biz', 'alias', 'name', 'bmodel', 'grade', 'sort',
                'internal', 'active', 'locked', 'replace']
    list_editable = ['active', 'locked', 'replace']
    list_filter = ['biz']
    fields = ['alias', 'name', 'grade', 'sort']
    inlines = [MdaViewLin1]


"""
class BRouteAdmin1(ModelAdmin1):
    list_display = ['alias_biz','alias', 'name', 'sort', 'bmodel', 'viewc', 
                        'active', 'internal', 'locked']
    list_filter = ['biz', 'active', 'internal', 'locked', 'viewc', 'bmodel']


    def alias_biz(self, obj):
        return obj.biz.alias
    
    def alias_bmodel(self, obj):
        if hasattr(obj, 'bmodel') and obj.bmodel:
            return obj.bmodel.alias
        else:
            return '---'

    def alias_viewc(self, obj):
        if hasattr(obj, 'viewc') and obj.bmodel:
            return obj.viewc.alias
        else:
            return '---'
    def alias_tempv(self, obj):
        if hasattr(obj, 'tempv') and obj.tempv:
            return obj.tempv.alias
        else:
            return '---'
"""
#--------------------------
if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Mda)
    admin.site.register(MdaAux)
    admin.site.register(MdaView)
    admin.site.register(MdaViewAux)
