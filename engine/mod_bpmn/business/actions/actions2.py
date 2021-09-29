# -*- coding: utf-8 -*-
from importlib import import_module
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.utils.base import print_msg
from mod_auth.adjango.models import Group, User, Permission, GroupProp, UserProp

from ..models import Biz
# from mod_bpmn.data.models import BApp, BModel
# from mod_bpmn.layouts.models import Component, CompProp, Layout
# from mod_bpmn.mdas.models import Mda, MdaAux, MdaView, MdaViewAux

def print_msg(msg):
    return print(msg)



#============================
# carga_ini personalizada
# ---------------------

def load_mdas(modeladmin, request, queryset):
    from mod_bpmn.data.models import BApp, BModel
    from mod_bpmn.layouts.models import Component, CompProp, Layout
    from mod_bpmn.mdas.models import Mda, MdaAux, MdaView, MdaViewAux
    load_Mda(modeladmin, request, queryset)
    # load_MdaAux(modeladmin, request, queryset)
    # load_MdaViewc(modeladmin, request, queryset) 

#----------------------------
# load_mdas: 4
#----------------------------

def load_Mda(modeladmin, request, queryset):
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 7.- load_mdas")
    print("-------------------")
    #-----------------------
    Mda.objects.filter(biz=biz).update(mark='N')
    replace = biz.replace
    add = True
    #------------------------ 
    def save_route(urlx, index=0, index1=0):
        name = getattr(urlx,'name', '')
        view = getattr(urlx, 'lookup_str', '' )
        path = getattr(urlx.pattern, '_route', '')
        # urlconf_name = getattr(urlx, 'urlconf_name', '')
        #------------------------------
        print("%s  name= %s   view= %s   path= %s" % (
            index, name, view, path))
        # import pdb; pdb.set_trace()
        #------------------------- 
        if not path:
            count = index+1
            count1 = 1
        else:
            count = index
            count1 = index1+1
        #--------------------
        if not name and path == '<path:object_id>/':
            return (index, index1)
            
        elif not name:
            name_list = []
        else:
            name_list = name.split('_')
        if len(name_list) > 1:
            try:
                ctt = ContentType.objects.get(app_label=name_list[0], model=name_list[1])
                mda_reg = modeladmin.admin_site._registry[ctt.model_class()] 
                alias_mda = ctt.model_class().__name__ # mda_reg.__class__.__name__
                name_mda = mda_reg.__class__.__name__
                bapp = BApp.objects.get(biz=biz, name=name_list[0])
                bmodel = BModel.objects.get(
                    bapp=bapp, alias="%s_%s" % (name_list[0],name_list[1]))
                grade_mda = '<Resource>' # name_list[0] # app_label
                tags_mda = view[:-len(view.split('.')[-1])]
                #----------------------
                alias_viewc = path
                name_viewc = 'changelist' if not path else path.split('/')[-2]
                grade_viewc = '<%s>' % (name_viewc)
                # grade_viewc = '<%s%s>' % (alias_mda, name_viewc)
                #------------------------


            except ContentType.DoesNotExist:
                return (index, index1)
        else:
            alias_mda = 'AdminSite1'  # .split('.')[-1]
            name_mda = 'AdminSite1'
            bmodel = None
            grade_mda = '<Admin>'
            tags_mda = view[:-len(view.split('.')[-1])]
            #------------------------
            alias_viewc = path
            # name_viewc = path[:-1]
            name_viewc = 'index' if not path else path[:-1]
            grade_viewc = '<%s>' % name_viewc
        #------------------------
        try:
            mda = Mda.objects.get(biz=biz, alias=alias_mda)
            if not biz.replace:
                mda.mark = 'S'
                mda.save(update_fields=['mark'])
        except Mda.DoesNotExist:
            if not add:
                return (index, index1)
            mda = Mda(biz=biz, alias=alias_mda)
        mda.name = name_mda
        mda.sort = "%03d" % count
        mda.bmodel = bmodel
        mda.grade = grade_mda # "%s_template" % alias_viewc
        mda.tags = tags_mda
        mda.locked = True
        mda.active = False
        mda.internal = True
        #---------------
        mda.mark = 'S'
        mda.date_time = timezone.now()
        #---------------- 
        mda.save()
        #----------------------------------
        # count1 = 0
        try:
            mdav = MdaView.objects.get(mda=mda, alias=alias_viewc)
            if not replace:
                mdav.mark ='S'
                mdav.save(update_fields=['mark'])
                return  (count, index1)
        except MdaView.DoesNotExist:
            if not add:
                return (count, index1)
            mdav = MdaView(mda=mda, alias=alias_viewc)
        # mdav.viewc = viewc
        mdav.name = name_viewc
        mdav.sort = "%03d_%02d" % (count, count1)
        mdav.grade = grade_viewc
        mdav.locked = True
        mdav.active = False
        mdav.internal = True
        #---------------
        mdav.mark = 'S'
        mdav.date_time = timezone.now()
        #---------------- 
        mdav.save()

        #------------------------
        comp = Component.objects.get(biz=biz, alias=grade_viewc)
        count2 = 0
        for prop in comp.compprop_set.all():
            count2 +=1
            try:
                mdavx = MdaViewAux.objects.get(mdaviewc=mdav, alias=prop.alias)
                if not replace:
                    mdav.mark ='S'
                    mdav.save(update_fields=['mark'])
                    continue  
            except MdaViewAux.DoesNotExist:
                if not add:
                    continue
                mdavx = MdaViewAux(mdaviewc=mdav, alias=prop.alias)  
            mdavx.name = prop.name
            mdavx.sort = "%03d_%02d_%03d" % (count, count1, count2)
            mdavx.save()          
        return (count, count1)
    #--------------------
    index = 0
    index1 = 0
    urls = modeladmin.admin_site.urls
    for url in urls[0]:
        if not getattr(url, 'urlconf_name', []):
            # count +=1
            index, index1 = save_route(url, index=index, index1=index1)
        else:
            print("Grupo de urls")
            print('--------------')
            for url1 in url.urlconf_name:
                # count +=1
                index, index1 = save_route(url1, index=index, index1=index1)
    #-----------------------------------
    Mda.objects.filter(biz=biz, mark='N').delete()
    print("-----------------")
    # load_mdasx(modeladmin, request, queryset)
    return
load_mdas.short_description = _("Load MDAS")

def load_MdaAux(modeladmin, request, queryset):
    #-----------------
    from .inidata import get_MdaX 
    print()
    print("BIZ 8.- load_MdaX")
    print("----------------------")
    #-----------------------
    value = get_MdaX()
    load_datamodel(MdaX,value,replace=False, add=True)
    print("-----------------")    
    return

def load_mdasx(modeladmin, request, queryset):
    # from .inidata import get_MdaX 
    biz = queryset[0]    
    #-----------------
    print()
    print("BIZ 8.- load_mdasx")
    print("-------------------")
    #-----------------------
    mda_regs = modeladmin.admin_site._registry
    for Modelreg, mda_reg in mda_regs.items():
        alias_mda = mda_reg.__class__.__name__    
        mda = Mda.objects.get(biz=biz, alias=alias_mda)
        if hasattr(mda_reg, 'inlines') and mda_reg.inlines:
            conta_inline = 0
            for inline in mda_reg.inlines:
                conta_inline +=1
                alias_mda1 = inline.__name__
                try:
                    mda1 = Mda.objects.get(biz=biz, parent=mda, alias=alias_mda1)
                except Mda.DoesNotExist:
                    mda1 = Mda(biz=biz, parent=mda, alias=alias_mda1)
                    mda1.save()
                

#===========================================
"""
def load_BizAux(modeladmin, request, queryset):
    from .inidata import get_BizX
    biz = queryset[0]
    Model = BizAux
    #-----------------
    print()
    print("BIZ 1.- load_BizX")
    print("-------------------")
    add = True
    #-----------------------
    if biz.locked:
        return (30, "CMS %s: bloqueado. No se puede cargar params" % biz.alias)
    args = get_BizAux()
    if not args:
        return (30, "No hay params para cargar en el SITIO %s:" % biz.alias)
    #----------------
    if not biz.active:
        BizAux.objects.filter(biz=biz).delete()
    else:
        BizX.objects.filter(biz=biz).update(mark='N')
    #-------------------
    count = 0
    for key, data in args.items():
        alias = key
        count +=1
        try:
            param = BizX.objects.get(biz=biz, alias=alias) # , grade=key[1])
            if not biz.replace:
                param.mark ='S'
                param.save(update_fields=['mark'])
                continue
        except BizX.DoesNotExist:
            param = BizX(biz=biz, alias=alias) # , grade=key[1])
        for attr, data1 in data.items():
            setattr(param, attr, data1)
        param.mark = 'S'
        param.date_time = timezone.now()
        param.save()
    #--------------------------------------
    BizX.objects.filter(biz=biz, mark='N').delete()
    return (25, "Biz %s: Creados %s params" % (biz.alias, count))

"""
