# -*- coding: utf-8 -*-
from ast import literal_eval
from importlib import import_module
from django.conf import settings
from django.contrib import messages
from django.db.models.fields import GenericIPAddressField
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.utils.base import print_msg
from mod_auth.adjango.models import Group, User, Permission, GroupProp, UserProp

from ..models import Company, CompanyProp, CompanyLoad, Menu, MenuItem


def print_msg(msg):
    return print(msg)


def ac_load_CompanyLoad(modeladmin, request, queryset):
    if request.user.is_superuser:      
        company = queryset[0]
        mensaje, level = company.load_CompanyLoad() 
        modeladmin.message_user(request, mensaje, level)     
    return 
#====================

def load_Company(modeladmin, request, obj):
    company = obj.company
    if not company.locked and company.replace:
        mod_dataload = import_module('%s.config.dataload' % settings.SITE_NAMEX)
        data = getattr(mod_dataload, 'DATA_COMPANY')
        if data:
            for campo in data.keys():
                setattr(company, campo, data[campo])
            company.save()
    return
load_Company.short_description = _("1.1._ Load Company") 


def load_CompanyProp(modeladmin, request, obj):
    company = obj.company 
    pass
load_CompanyProp.short_description = _("1.1.1._ Load CompanyProp") 



def load_rols(modeladmin, request, obj):
    company = obj.company
    replace = company.replace
    add = True
    #-------
    mod_setmenu = import_module('%s.config.setmenu' % settings.SITE_NAMEX)
    get_menus = getattr(mod_setmenu, 'get_MENUS')
    menus = get_menus()
    # import pdb; pdb.set_trace()
    #-------------------------
    count = 0
    mensaje = ''   
    companies = [company] 
    for company in companies:
        if settings.SITE_NAME != company.alias:
            mensaje += _("Sólo se puede cargar el sitio propio: %s") % settings.SITE_NAME
            modeladmin.message_user(request, mensaje, messages.WARNING)
            return
        #--------------
        count = 0
        for menu_name, menu_config in menus.items():
            count +=1
            name = menu_name
            try:
                group = Group.objects.get(name=name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=name)
            #---------------
            filtro_perm = menu_config[2]
            # import pdb; pdb.set_trace()
            if filtro_perm:
                perms = list(Permission.objects.filter(**filtro_perm))
            else:
                perms = list(Permission.objects.all())
            group.permissions.set(perms)
            group.save()
            try:
                user = User.objects.get(username=name.lower())
            except User.DoesNotExist:
                user = User.objects.create_user(
                    is_staff=True,
                    username=name.lower(),
                    password='_%s' % name.lower()
                    )
            user.groups.add(group)
            user.save()
            try:
                user_prop = UserProp.objects.get(user=user, alias='rol_menu', name=name)
            except UserProp.DoesNotExist:
                user_prop = UserProp(user=user, alias='rol_menu', name=name)
            user_prop.save()                           
        mensaje = _("Rols de %s creados") % (count)
        modeladmin.message_user(request, mensaje, messages.SUCCESS)        
    return
load_rols.short_description = _("1.2._ Load Rols")





def load_menu(modeladmin, request, obj, rol_menu=None):
    company = obj.company
    replace = company.replace
    msg = _("Cargado Menú")
    total = 0

    try:
        menu = Menu.objects.get(company=company, 
                            rol_menu=rol_menu, user=None,
                            alias="%s_%s" % (company.alias, 'General' if not rol_menu else "%s" % rol_menu.name))
        if not replace:
            menu.mark='S'
            menu.save(update_fields=['mark'])
    except Menu.DoesNotExist:
        menu = Menu.objects.create(company=company, 
                                rol_menu=rol_menu, user=None,
                                alias="%s_%s" % (company.alias, 'General' if not rol_menu else "%s" % rol_menu.name))
    menu.name = _("Menú General") if not rol_menu else _("Menú de %s" % rol_menu)
    menu.save()
    #-----------------
    try:
        menu_item0 = MenuItem.objects.get(menu=menu, parent=None, grade='00', sort='00', 
                                alias=menu.alias)
        if not replace:
            menu_item0.mark='S'
            menu_item0.save(update_fields=['mark'])
    except MenuItem.DoesNotExist:
        menu_item0 = MenuItem.objects.create(menu=menu, parent=None, grade='00', sort='00', 
                                alias=menu.alias)
    # menu_item0.grade = "00"
    # menu_item0.sort = "00"
    menu_item0.save()
    #-------------------
    count = 0
    for fila in settings.MODELADMINS:
        if not '.apps.' in fila[0]:
            app = fila[0] # module
        else:
            app = fila[0][:fila[0].index('.apps.')]
        path = "/%s/%s/" % (settings.SITE_NAME, app)

        count +=1
        print_msg("%02d: %s" % (count, app)) 
        try:
            menu_app = MenuItem.objects.get(menu=menu, parent=menu_item0, path=path,
                    alias=app, grade="%02d" % count, sort='00')
            if not replace:
                menu_app.mark='S'
                menu_app.save(update_fields=['mark'])

        except MenuItem.DoesNotExist:
            menu_app = MenuItem(menu=menu, parent=menu_item0, path=path,
                    alias=app, grade="%02d" % count, sort='00')
        menu_app.name = app
        # menu_app.grade = "%02d" % count
        # menu_app.sort = "%02d" % 0
        menu_app.save()
        #------------------------
        try:
            app_models = import_module("%s.models" % app)
        except ImportError as exc:
            msg = exc.args[0]
            print_msg("ERROR!!!: la app %s no tiene models. %s" % (app, msg))
            continue
        count1 = 0
        for fila1 in fila[1]: # [Model, modelAdmin, en_Menu]
            count1 +=1  
            Model = getattr(app_models, fila1[0])
            path = "/%s/%s/%s/" % (settings.SITE_NAME, Model._meta.app_label, Model._meta.model_name)
            print_msg("%02d %02d: %s" % (count, count1, path)) 
            try:
                menu_mda = MenuItem.objects.get(menu=menu, parent=menu_app, alias=fila1[1], path=path, grade="%02d" % count, sort="%02d" % count1)
                if not replace:
                    menu_mda.mark='S'
                    menu_mda.save(update_fields=['mark'])
            except MenuItem.DoesNotExist:
                menu_mda = MenuItem(menu=menu, parent=menu_app, alias=fila1[1], path=path, grade="%02d" % count, sort="%02d" % count1)

            menu_mda.name = Model._meta.verbose_name_plural
            # menu_mda.grade = "%02d" % count
            # menu_mda.sort = "%02d" % count1
            menu_mda.save()
            #------------------------
        total += count1
    total += count
    mensaje = "%s %s: %s options" % (msg, "General" if not rol_menu else "General de %s" % rol_menu.name, total)
    # modeladmin.message_user(request, mensaje, messages.SUCCESS)        
    return (mensaje, messages.SUCCESS)

#----------------------------
# load menus
#----------------------------

def load_general_menu(modeladmin, request, obj):
    mensaje, level = load_menu(modeladmin, request, obj=obj, rol_menu=None)
    modeladmin.message_user(request, mensaje, level)  
load_general_menu.short_description = _("Load General Menu")


def load_rol_menus(modeladmin, request, obj):
    company= obj.company
    replace = company.replace
    add = True
    #-------
    mod_setmenu = import_module('%s.config.setmenu' % settings.SITE_NAMEX)
    get_menus = getattr(mod_setmenu, 'get_MENUS')
    menus = get_menus()
    # import pdb; pdb.set_trace()
    #-------------------------
    count = 0
    mensaje = ''   
    companies = [company] 
    for company in companies:
        if settings.SITE_NAME != company.alias:
            mensaje += _("Sólo se puede cargar el sitio propio: %s") % settings.SITE_NAME
            modeladmin.message_user(request, mensaje, messages.WARNING)
            return
        #--------------
        count = 0
        
        for menu_name, menu_config in menus.items():
            count +=1

            name = menu_name
            group = Group.objects.get(name=name)

            if not menu_config[1]:
                mensaje, level = load_menu(modeladmin, request, obj=obj, rol_menu=group)
            else:
                try:
                    menu = Menu.objects.get(company=company, rol_menu=group, user=None,
                                            alias=name)
                except Menu.DoesNotExist:
                    menu = Menu.objects.create(company=company, rol_menu=group, user=None,
                                            alias=name)
                    #  menu.save()
                menu.name = _("Menú de %s" % group.name)
                menu.save()
                #----------------------
                try:
                    menu_item0 = MenuItem.objects.get(menu=menu, alias=menu.alias)
                    if not replace:
                        menu_item0.mark='S'
                        menu_item0.save(update_fields=['mark'])
                except MenuItem.DoesNotExist:
                    if not add:
                        continue
                    menu_item0 = MenuItem.objects.create(menu=menu, alias=menu.alias)
                # menu.index_url = menu_config[0]
                # menu_item0.grade = "00"
                # menu_item0.sort = "00"
                menu_item0.save()
                #--------------
                count = 0
                total = 0
                for app in menu_config[1]:
                    # app[0] = [app_url, app_titulo]
                    # app[1] = [[opcion_url, opcion_titulo],[...],]
                    count +=1
                    if app[0][0].startswith('='):
                        path_app = app[0][0][1:]
                    else:
                        # path_app = "%s%s" % (settings.PREFIX_URL, app[0][0])
                        path_app = app[0][0]
                    name_app = app[0][1]
                    
                    try:
                        menu_app = MenuItem.objects.get(menu=menu, parent=menu_item0, alias=path_app, 
                                                        path=path_app, grade="%02d" % count, sort="00")
                        if not replace:
                            menu_app.mark='S'
                            menu_app.save(update_fields=['mark'])
                    except MenuItem.DoesNotExist:
                        if not add:
                            continue
                        menu_app = MenuItem(menu=menu, parent=menu_item0, alias=path_app, 
                                                        path=path_app, grade="%02d" % count, sort="00")
                    menu_app.name = name_app
                    # menu_app.grade = "%02d" % count
                    # menu_app.sort = "%02d" % 0
                    menu_app.save()
                    #-----------------
                    count1 = 0
                    for option in app[1]:
                        count1 +=1
                        # path_option = option[0]
                        if option[0].startswith('='):
                            path_option = option[0][1:]
                        else:
                            # path_option = "%s%s" % (settings.PREFIX_URL, option[0])
                            path_option = option[0]
                        name_option = option[1]
                        try:
                            menu_option = MenuItem.objects.get(menu=menu, parent=menu_app, alias=path_option, 
                                                            path=path_option, grade="%02d" % count, sort="%02d" % count1)
                        except MenuItem.DoesNotExist:
                            menu_option = MenuItem(menu=menu, parent=menu_app, alias=path_option, 
                                                            path=path_option, grade="%02d" % count, sort="%02d" % count1)
                            menu_option.save()  
        
                        menu_option.name = name_option
                        menu_option.grade = "%02d" % count
                        # menu_option.sort = "%02d" % count1
                        menu_option.save()
                    total += count1
                total += count                               
                mensaje = _("Menu/Rol de %s: creadas %s opciones") %(group.name, total)
                level = messages.SUCCESS
            modeladmin.message_user(request, mensaje, level)        
    return
load_rol_menus.short_description = _("Load Rol Menus")

#--------------
# DocType
#--------------

def load_DocType(modeladmin, request, obj):
    company = obj.company
load_DocType.short_description = _("Load DocType") 


#====================

def load_Project(modeladmin, request, obj):
    from mod_auth.doctypes.models import DocType
    from mod_entity.projects.models import Project
    company = obj.company
    mod_dataload = import_module('%s.config.dataload' % settings.SITE_NAMEX)
    data = getattr(mod_dataload, 'DATA_PROJECT')

    #-----------
    for data_row in data:
        alias = data_row[0]
        dt_alias = data_row[1]
        params = data_row[2]
        try:
            dt = DocType.objects.get(model_name='Project', company=company, alias=dt_alias)
        except DocType.DoesNotExist:
            dt = DocType(model_name='Project', company=company, alias=dt_alias)
            dt.save()
        try:
            project = Project.objects.get(doctype=dt, alias=alias)
        except Project.DoesNotExist:
            project = Project(doctype=dt, alias=alias)
            project.save()
        if params:
            for k,valor in params.items():
                setattr(project, k, valor)
        project.save()
