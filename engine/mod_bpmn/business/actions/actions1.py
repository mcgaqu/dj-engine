# -*- coding: utf-8 -*-
import os, sys
from importlib import import_module
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from mod_admin.utils.loaddata import load_datamodel, load_datamodelx
from mod_auth.adjango.models import Group, User, Permission
from mod_bpmn.data.models import Database, BApp, BModel, BModelField, BModelAction
from mod_bpmn.datastate.models import BAction, BReducer
from mod_bpmn.layouts.models import Component, CompProp, Layout


from ..models import Biz

def load_BPMN(modeladmin, request, queryset):
    load_data(modeladmin, request, queryset)
    load_datastate(modeladmin, request, queryset)
    load_layouts(modeladmin, request, queryset)
    # load_mdas(modeladmin, request, queryset)
    # load_cocklists(modeladmin, request, queryset)
    # load_tasklist(modeladmin, request, queryset)

def load_data(modeladmin, request, queryset):
    from mod_bpmn.data.models import Database, BApp, BModel, BModelField, BModelAction
    load_Bapp(modeladmin, request, queryset)
    load_BModel(modeladmin, request, queryset)


def load_datastate(modeladmin, request, queryset):
    pass

def load_layouts(modeladmin, request, queryset):
    from mod_bpmn.layouts.models import Component, CompProp, Layout
    load_Component(modeladmin, request, queryset)
    # load_Layout((modeladmin, request, queryset))




#----------------------------
# load_apps: 1.1
#----------------------------
def load_Bapp(modeladmin, request, queryset):
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 1.1.- load_apps")
    print("-----------------")
    #-----------------------
    BApp.objects.filter(biz=biz).update(mark='N')
    replace = biz.replace
    add = True
    #------------------------
    apps = settings.INSTALLED_APPS
    count = 0
    for name in apps:
        count +=1
        print(count, name)
        if not '.apps.' in name:
            alias = name # module
        else:
            alias = name[:name.index('.apps.')]
        grade = alias.split('.')[-1]
        internal = False if alias.startswith('mod_') else True
        try:
            bapp = BApp.objects.get(biz=biz, alias=alias)
            if not replace:
                bapp.mark ='S'
                bapp.save(update_fields=['mark'])
                continue
        except BApp.DoesNotExist:
            if not add:
                continue
            bapp = BApp(biz=biz, alias=alias)
        bapp.alias = alias    
        bapp.sort = "%02d" % count
        bapp.grade = grade
        bapp.locked = True
        bapp.active = False
        bapp.internal = internal
        #---------------
        bapp.mark = 'S'
        bapp.date_time = timezone.now()
        #----------------
        bapp.save()
    BApp.objects.filter(biz=biz, mark='N').delete()
    mensaje = _("%s Aplicaciones cargadas") % count
    modeladmin.message_user(request, mensaje, messages.SUCCESS)  
    return

#----------------------------
# load_models: 1.2
#----------------------------
def load_BModel(modeladmin, request, queryset):
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 1.2.- load_models")
    print("-------------------")
    #-----------------------
    BModel.objects.filter(biz=biz).update(mark='N')
    replace = biz.replace
    add = True
    #------------------------    
    ctts = ContentType.objects.all()
    count = 0
    for ctt in ctts:
        count +=1
        print(count, ctt.app_label, ctt.model)
        try:
            bapp = BApp.objects.get(biz=biz, grade=ctt.app_label)
        except BApp.DoesNotExist:
            continue
        #----------------
        Model = ctt.model_class()
        # import pdb; pdb.set_trace()
        
        alias = Model.__name__
        # capfirst(Model._meta.verbose_name_plural)
        name = Model._meta.verbose_name_plural

        try:
            bmodel = BModel.objects.get(biz=biz, alias=alias)
            if not replace:
                bmodel.mark ='S'
                bmodel.save(update_fields=['mark'])
                continue 
        except BModel.DoesNotExist:
            if not add:
                continue
            bmodel = BModel(biz=biz, alias=alias)
        bmodel.bapp = bapp
        bmodel.name = name
        bmodel.sort = "%03d" % (count)
        bmodel.grade = ctt.app_label
        bmodel.locked = True
        bmodel.active = False
        bmodel.internal = True
        #---------------
        bmodel.mark = 'S'
        bmodel.date_time = timezone.now()
        #----------------
        bmodel.save()
        fields = Model._meta.concrete_fields
        for field in fields:
            alias_field = field.name
            try:
                mf = BModelField.objects.get(bmodel=bmodel, alias=alias_field)
            except BModelField.DoesNotExist:
                mf = BModelField(bmodel=bmodel, alias=alias_field)
                mf.save()
        #----------------------
        module_actions = bapp.get_module('actions')
        if module_actions and hasattr(module_actions, 'get_app_actions'):
            get_app_actions = getattr(module_actions, 'get_app_actions')
            actions = get_app_actions(bmodel.alias)
            for action in actions:
                try:
                    bmac = BModelAction.objects.get(bmodel=bmodel, alias=action)
                except BModelAction.DoesNotExist:
                    bmac = BModelAction(bmodel=bmodel, alias=action)
                    bmac.save()
        
        #-------------------------
    BModel.objects.filter(biz=biz, mark='N').delete()
    mensaje = _( "%s BModels loaded") % count
    modeladmin.message_user(request, mensaje, messages.SUCCESS)  
    return 

#----------------------------
# load_datastate: 2
#----------------------------

#----------------------------
# load_layouts: 3
#----------------------------
#----------------------------
# load_components: 3.1
#----------------------------

def load_Component(modeladmin, request, queryset):
    # from .inidata import  get_components  # , get_Layout
    from mod_bpmn.layouts.inidata import  get_components
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 3.1.- load_components")
    print("-------------------")
    replace = biz.replace
    add = True
    #-----------------------
    for front in ['django', 'flutter']:
        Component.objects.filter(biz=biz, grade=front).update(mark='N')
        items = get_components(front)
        total = 0
        count = 0
        for item in items:
            count +=1
            try:
                comp = Component.objects.get(biz=biz, grade=front, alias=item[0])
                if not replace:
                    comp.mark='S'
                    comp.save(update_fields=['mark'])
            except Component.DoesNotExist:
                if not add:
                    continue
                comp = Component(biz=biz, grade=front, alias=item[0])
            comp.sort = '%02d' % count
            #---------------
            # comp.grade = front
            comp.mark = 'S'
            comp.date_time = timezone.now()
            comp.save()
            #--------------------------
            # import pdb; pdb.set_trace()
            count1 = 0        
            if (len(item)<2 or len(item[1]) == 0):
                continue
            for key, value in item[1].items():
                count1 +=1
                try:
                    prop = CompProp.objects.get(component=comp, alias=key)
                    if not replace:
                        prop.mark='S'
                        prop.save(update_fields=['mark'])
                except CompProp.DoesNotExist:
                    if not add:
                        continue
                    prop = CompProp(component=comp, alias=key)
                prop.name = value
                # prop.name = "{%s%s}" % (prop.alias[0].capitalize(), prop.alias[1:])
                prop.sort = "%02d_%02d" % (count, count1)
                #---------------- 
                prop.mark = 'S'
                prop.date_time = timezone.now()
                prop.save()
            total += count1
        #-----------------------
        Component.objects.filter(biz=biz, grade=front, mark='N').delete()
        mensaje = _("%s Componentes cargados de %s") % (total, front)
        modeladmin.message_user(request, mensaje, messages.SUCCESS)  
    return

#----------------------------
# load_Layout: 3.2
#----------------------------
def load_Layout(modeladmin, request, queryset):
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 3.2.- load_Layout")
    print("-------------------")
    #-----------------------
    Layout.objects.filter(biz=biz).update(mark='N')
    replace = biz.replace
    add = True
    #------------------------ 
    mod_setconf = import_module('%s.setconf' % settings.SITE_NAME)
    MDA_APPS = getattr(mod_setconf, 'MDA_APPS')
    #-------------------------
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
            #------------------------
            app_label = name_list[0]
            if app_label not in MDA_APPS:
                return (index, index1)
            try:
                
                ctt = ContentType.objects.get(app_label=name_list[0], model=name_list[1])                  
                mda_reg = modeladmin.admin_site._registry[ctt.model_class()] 
                alias_mda = ctt.model_class().__name__ # mda_reg.__class__.__name__
                name_mda = mda_reg.__class__.__name__
                # bapp = BApp.objects.get(biz=biz, name=name_list[0])
                bmodel = BModel.objects.get(
                    biz=biz, alias="%s_%s" % (name_list[0],name_list[1]))
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
            mda = Layout.objects.get(biz=biz, alias=alias_mda)
            if not biz.replace:
                mda.mark = 'S'
                mda.save(update_fields=['mark'])
        except Layout.DoesNotExist:
            if not add:
                return (index, index1)
            mda = Layout(biz=biz, alias=alias_mda)
        mda.name = name_mda
        mda.sort = "%03d" % count
        # mda.bmodel = bmodel
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
            mdav = Layout.objects.get(biz=biz, parent=mda, alias=alias_viewc)
            if not replace:
                mdav.mark ='S'
                mdav.save(update_fields=['mark'])
                return  (count, index1)
        except Layout.DoesNotExist:
            if not add:
                return (count, index1)
            mdav = Layout(biz=biz, parent=mda, alias=alias_viewc)
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
                mdavx = Layout.objects.get(biz=biz, parent=mdav, alias=prop.alias)
                if not replace:
                    mdav.mark ='S'
                    mdav.save(update_fields=['mark'])
                    continue  
            except Layout.DoesNotExist:
                if not add:
                    continue
                mdavx = Layout(biz=biz, parent=mdav, alias=prop.alias)  
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
    lays = Layout.objects.all()
    for lay in lays:
        try:
            comp = Component.objects.get(biz=biz, alias=lay.grade)
            lay.comp = comp
            lay.save(update_fields=['comp'])
        except Component.DoesNotExist:
            pass
            # comp = Component(biz=biz, alias=lay.grade)
            # comp.save()
    #-------------------------------------
    Layout.objects.filter(biz=biz, mark='N').delete()
    print("-----------------")
    # load_mdasx(modeladmin, request, queryset)
    return

