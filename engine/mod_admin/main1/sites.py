# -*- coding: utf-8 -*-
import datetime
from importlib import import_module
from weakref import WeakSet

from django.contrib import admin
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext as _, gettext_lazy


from mod_admin.utils.base import print_msg

# from .actions import (
#     delete1_selected,
#     save1_selected,
#     ac_export_changelist_csv,
#     ac_export_changelist_pdf,
#     ac_export_selected_csv,
#     ac_export_selected_pdf
#     )
    
    
all_sites = WeakSet()

class AdminSite1(admin.AdminSite):
    # Text to put at the end of each page's <title>. ZZ
    # site_title =  gettext_lazy('%s site admin' % settings.SITE_NAME)
    
    # Text to put in each page's <h1>.
    # site_header = gettext_lazy('%s administration' % settings.SITE_NAME)
    site_header = "Administración de: %s" % settings.SITE_NAME.upper()
    
    # Text to put at the top of the admin index page.
    # index_title = gettext_lazy('Site administration')
    
    # URL for the "View site" link at the top of each admin page.
    # site_url = '/'
    site_url = '/%s' % settings.PREFIX_URL
    


    def __init__(self, name='admin'):
        #------------------------------
        # super().__init__(name)
        self._registry = {}
        self.name = name
      
        self._actions = {
            'delete_selected': admin.actions.delete_selected,
        #     'delete1_selected': delete1_selected,
        #     'save1_selected': save1_selected,
        #     'ac_export_changelist_csv': ac_export_changelist_csv,
        #     'ac_export_changelist_pdf': ac_export_changelist_pdf,
        #     'ac_export_selected_csv': ac_export_selected_csv,
        #     'ac_export_selected_pdf': ac_export_selected_pdf
            }
        self._global_actions = self._actions.copy()
        # ------------------------------
        site = None
        if settings.SITE_ID:
            try:
                from django.contrib.sites.models import Site
                try:
                    site = Site.objects.get(pk=settings.SITE_ID)
                    if settings.SITE_NAME != site.name:
                        site.name = settings.SITE_NAME
                        site.domain = '%s.mcunita.github.com' % settings.SITE_NAME
                        site.save()
        
                    print_msg(" 1) Existe Site %s %s: %s" % (site.id, site.name, site.domain))
                except Site.DoesNotExist:
                    print_msg(" 1) No Existe Site %s %s: %s" % (site.id, site.name, site.domain))
            except:
                print_msg(" 1) No puedo importar: django.contrib.sites.models import Site")
        else:
            print_msg(" 1) No procede Crear Site ID: %s" % settings.SITE_ID)

        self.site = site
        all_sites.add(self)
        #-----------------------
        from django.contrib.auth.models import User, Group
        from mod_auth.adjango.models import UserProp
        from mod_auth.companies.models import Company
        try:
            user_site = User.objects.get(username=settings.SITE_NAME)
            print_msg(" 2) Existe Superusuario SITE_NAME: %s" % user_site.username)
        except User.DoesNotExist:
            user_site = User.objects.create_superuser(username=settings.SITE_NAME,
                    email='mc@multiges.net', password="_%s" % settings.SITE_NAME)
            print_msg(" 2) Creado Superusuario SITE_NAME: %s" % settings.SITE_NAME)
        try:
            user_prop = UserProp.objects.get(user=user_site, alias='rol_menu')
        except UserProp.DoesNotExist:
            user_prop = UserProp(user=user_site, alias='rol_menu', 
                name='%s_MASTER' % settings.SITE_NAME)
        user_prop.save()   

        #------------------
        try:
            company = Company.objects.get(id=settings.COMPANY_ID)
            print_msg(" 3) Existe Company ID: %s" % company.id)
        except Company.DoesNotExist:
            company = Company(id=settings.COMPANY_ID, internal=True,
                alias=settings.SITE_NAME)
            company.save()
            company.load_CompanyLoad()
            print_msg(" 3) Creada Company ID: %s" % company.id)
        self.company = company

        #----------------
        if settings.BIZ_ID:
            from mod_bpmn.business.models import Biz
            try:
                biz = Biz.objects.get(id=settings.BIZ_ID)
                print_msg(" 4) Existe Business ID: %s" % biz.id)
            except Biz.DoesNotExist:
                biz = Biz(id=settings.BIZ_ID, alias=settings.SITE_NAME, grade='django')
                biz.save()
                print_msg(" 4) Creado Business SITE_NAME: %s" % biz.id)
            self.biz = biz
        else:
            print_msg(" 4) No procede Crear Business ID: %s" % settings.BIZ_ID)
        self.site_header = self.get_site_header()
        return

    def get_site_header(self):
        if self.company.avatar:
            return "Admin"
        else:
            return self.site_header


    def register_models(self):        
        # import pdb; pdb.set_trace()
        count = 0
        print_msg("REGISTRAR MODELOS con NUM_ADMIN_SITE %s" % (settings.NUM_ADMIN_SITE))

        for fila in settings.MODELADMINS:
            if not '.apps.' in fila[0]:
                app = fila[0] # module
                # en el 2 -- fila[0] es alias
            else:
                app = fila[0][:fila[0].index('.apps.')]
            # app_label = module.split('.')[-1]
            count +=1
            print_msg("%02d: %s" % (count, app)) 
            try:
                app_models = import_module("%s.models" % app)
            except ImportError as exc:
                msg = exc.args[0]
                print_msg("ERROR!!!: la app %s no tiene models. %s" % (app, msg))
                continue
            try:
                app_admin = import_module("%s.admin" % app)
            except ImportError as exc:
                msg = exc.args[0]
                print_msg("ERROR!!!: la app %s no tiene admin. %s" % (app, msg))
                continue
            count1 = 0
            for fila1 in fila[1]: # [Model, modelAdmin]
                # import pdb; pdb.set_trace()
                count1 +=1  
                print_msg("%s %02d_%02d: %s" % ('   ', count, count1, fila1[0]))
                self.register(getattr(app_models, fila1[0]),  getattr(app_admin, fila1[1]))          

    

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        #-------------------
        menu_dict = {}
        count = 0
        for fila in settings.MODELADMINS:
            if not '.apps.' in fila[0]:
                app = fila[0] # module
            else:
                app = fila[0][:fila[0].index('.apps.')]
            count +=1
            print_msg("%02d: %s" % (count, app)) 
            try:
                app_models = import_module("%s.models" % app)
            except ImportError as exc:
                msg = exc.args[0]
                print_msg("ERROR!!!: la app %s no tiene models. %s" % (app, msg))
                continue
            count1 = 0
            for fila1 in fila[1]: # [Model, modelAdmin, en_Menu]
                count1 +=1  
                # print_msg("%s %02d_%02d: %s" % ('   ', count, count1, fila1[0]))
                Model = getattr(app_models, fila1[0])
                path = "/%s/%s/%s/" % (settings.SITE_NAME, Model._meta.app_label, Model._meta.model_name)
                # print_msg(path)
                menu_dict[path] = fila1[2]
        index_app = -1
        for xx in app_list:
            index_app +=1
            # print(xx) # app = cabecera + modelos
            xm = xx.get('models',[])
            index_model = -1
            for mm in xm:
                index_model +=1
                admin_url = mm['admin_url']
                # print(index_app, index_model, admin_url)
                num = menu_dict.get(admin_url, 0)
                if num == 0:
                    # print("quitar %s" % xx) 
                    # mantiene las opciones no registradas 
                    # + los modeladmin registrados con fila1[2]=1
                    del app_list[index_app]['models'][index_model]
        return app_list

    
    def x_get_userprop(self, user, alias_prop):
        return   

    def get_rol_menu(self, request):
        from django.contrib.auth.models import Group
        from mod_auth.adjango.models import UserProp

        # import pdb; pdb.set_trace()
        user = request.user
        dev = None
        #----------------
        if user.is_anonymous:
            name_rol = "WEBPUBLICA"

        elif hasattr(user, 'userprop_set'):
            try:
                name_rol = user.userprop_set.get(alias='rol_menu', active=True).name
            except UserProp.DoesNotExist:
                if user.is_superuser:
                    name_rol = 'MASTER'
                else:
                    name_rol = None
        #------------------
        if name_rol:
            try:
                dev = Group.objects.get(name=name_rol)
            except Group.DoesNotExist:
                if user.groups.count():
                    dev = user.groups.all()[0]
        return dev


    def menu_list(self, request):
        # import pdb; pdb.set_trace()
        from mod_auth.companies.models import Menu, MenuItem
        #-------------------------
        # Menu de la sesion
        #---------------------------
        key_session = "menu_%s_%s" % (request.user.username, settings.SITE_NAME)
        menu_list = request.session.get(key_session, [])
        if menu_list:
            return menu_list
        # menu_list = []
        
        menu = None
        #-----------------------------
        # Menu del usuario
        #--------------------
        if not request.user.is_anonymous:
            try:
                menu = Menu.objects.get(company=self.company, user=request.user, active=True)
            except Menu.DoesNotExist:
                pass
        #----------------------
        # Menu del rol
        #---------------------
        if not menu:
            rol_menu = self.get_rol_menu(request)
            if rol_menu:
                try:
                    menu = Menu.objects.get(company=self.company, rol_menu=rol_menu, active=True)
                except Menu.DoesNotExist:
                    pass
        #----------------
        if menu:
            apps = MenuItem.objects.filter(menu=menu, level=1).order_by('sort')
            for app in apps:
                option_list = []
                options = MenuItem.objects.filter(parent=app, active=True).order_by('sort')
                for option in options: # app.children.filter(ative=True):
                    option_list.append([option.path, option.name])
                app_list = [[app.path, app.name], option_list]
                menu_list.append(app_list)
            print(menu_list)
            return menu_list
        #-----------------------
        # Menu de la setmenu.py
        #---------------------------
        if rol_menu:
            mod_setmenu = import_module('%s.config.setmenu' % settings.SITE_NAMEX)
            get_menus = getattr(mod_setmenu, 'get_MENUS')
            menus = get_menus()
            #------------------------  
            name_rol = rol_menu.name
            menu_list = menus[name_rol][1]
            #---------------
            # Añadir menus personalizados
        #----------------------
        if False:
            username = request.user.username
            hoy = datetime.date.today()
            sufijo = "?agente1__alias=%s&fecha1__gte%s" % (username, hoy)
            menu_list.append(
                [
                    ['%sproyex/hito/%s' % (settings.PREFIX_URL, hoy), 'Hitos Pendientes de Vencer'],
                    [],
                ]
            )
        #---------------------
        print(menu_list)
        return menu_list

    def each_context(self, request):
        # import pdb; pdb.set_trace()
        return {
            **(super().each_context(request)),
            'menu_cms': self.menu_list(request),
           # 'rol_menu': self.get_rol_menu(request),
        }

    def x_get_urls(self):
        dev = super().get_urls()
        print(dev[-1])
        import pdb; pdb.set_trace()
        return dev


    def get_index_url(self, request):
        rol_menu = self.get_rol_menu(request)
        menus = rol_menu.menu_set.all()
        if menus:
            menu = menus[0]
            menuitem0 = menu.menuitem_set.get(level=0).path
            return menuitem0
        return None

    def index(self, request, extra_context=None):
        if self.get_index_url(request):
            return HttpResponseRedirect(self.get_index_url(request))
        else:
            return super().index(request, extra_context)
