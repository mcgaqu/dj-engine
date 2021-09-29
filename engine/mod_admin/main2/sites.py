# -*- coding: utf-8 -*-

from importlib import import_module
from django.conf import settings
from django.contrib import admin
from mod_admin.main1.sites import AdminSite1
from mod_admin.utils.base import print_msg

class AdminSite2(AdminSite1):


    # def __init__(self, name='admin'):
    #     #------------------------------
    #     # super().__init__(name)
    def _build_app_dict(self, request, label=None):
        from mod_auth.business.models import Rol, RolMenu
        if request.user.groups:
            rol = request.user.groups.all()[0]
        else:
            rol = Rol.objects.get(biz=self.biz, alias='MANAGER')
        #---------------------------
        from mod_base.mdas.models import Mda
        # app_list = super().get_app_list(request)
        app_dict0 = super()._build_app_dict(request)
        app_dict = {}
        # import pdb; pdb.set_trace()
        count = 0
        for app_label, app_data0 in app_dict0.items():
            bapp = BApp.objects.get(biz=self.biz, name=app_label)
            count +=1
            if bapp.active:
                app_data = app_data0.copy()
                print('APP activa = ', app_data.keys())
                models_list = app_data['models']
                app_data['models'] = []
                index_model = -1
                for model_dict in models_list:
                    index_model +=1
                    # print("   model %s %s %s" % (count, index_model, model_dict['admin_url']))
                    admin_url_list = model_dict['admin_url'].split('/')
                    alias_bmodel = "%s_%s" % (admin_url_list[-3], admin_url_list[-2])
                    mda = Mda.objects.get(internal=True, bmodel__alias=alias_bmodel)
                    # print("   mda   %s %s  = %s  %s" % (count, index_model, alias_bmodel, mda.alias))
                    if mda.active:
                        app_data['models'].append(model_dict)
                if app_data['models']:
                    app_dict[app_label] = app_data
            else:
                print('APP NO activa = %s' % app_label)
        # print(app_dict)
        return app_dict


    def x_build_app_dict(self, request, label=None):
        from mod_base.data.models import BApp
        from mod_base.mdas.models import Mda
        # app_list = super().get_app_list(request)
        app_dict0 = super()._build_app_dict(request)
        app_dict = {}
        # import pdb; pdb.set_trace()
        count = 0
        for app_label, app_data0 in app_dict0.items():
            bapp = BApp.objects.get(biz=self.biz, name=app_label)
            count +=1
            if bapp.active:
                app_data = app_data0.copy()
                print('APP activa = ', app_data.keys())
                models_list = app_data['models']
                app_data['models'] = []
                index_model = -1
                for model_dict in models_list:
                    index_model +=1
                    # print("   model %s %s %s" % (count, index_model, model_dict['admin_url']))
                    admin_url_list = model_dict['admin_url'].split('/')
                    alias_bmodel = "%s_%s" % (admin_url_list[-3], admin_url_list[-2])
                    mda = Mda.objects.get(internal=True, bmodel__alias=alias_bmodel)
                    # print("   mda   %s %s  = %s  %s" % (count, index_model, alias_bmodel, mda.alias))
                    if mda.active:
                        app_data['models'].append(model_dict)
                if app_data['models']:
                    app_dict[app_label] = app_data
            else:
                print('APP NO activa = %s' % app_label)
        # print(app_dict)
        return app_dict
    
    #======================

    def get_mdaviewc(self, request, mdaviewc_id=0):
        from mod_base.mdas.models import MdaViewc
        mdaviewc = MdaViewc.objects.get(id=mdaviewc_id)
        return mdaviewc

    def get_extra_context(self, request, mdaviewc_id=0):
        if not mdaviewc_id:
            return {}
        mdaviewc = self.get_mdaviewc(request, mdaviewc_id)
        if not mdaviewc:
            return {}
        dev = {}
        layout = mdaviewc.layout
        for lh in layout.children.filter(active=True):
            compxs = lh.component.datax_set.filter(active=True)
            for compx in compxs:
                dev[compx.alias] = compx.valuex
        return

    # @never_cache
    def x_index(self, request, mdaviewc_id, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        extra_context = self.get_extra_context(request, mdaviewc_id=mdaviewc_id)
        return super().index(self, request, extra_context)
    

    @never_cache
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)


"""
import os, json, datetime
from importlib import import_module
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse

from .utils.base import print_msg, get_cms, get_emp 
from .actions.crud import delete1_selected, save1_selected



class AdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>. ZZ
    site_title = settings.SITE_NAME # ugettext_lazy('Django site admin')

    # Text to put in each page's <h1>.
    site_header = settings.SITE_NAME # ugettext_lazy('Django administration')

    # Text to put at the top of the admin index page.
    index_title = settings.SITE_NAME # ugettext_lazy('Site administration')

    # URL for the "View site" link at the top of each admin page.
    # site_url = '/'
    site_url = '/%s' % settings.PREFIJO_URL

    index_template = None

    def __init__(self, name='admin'):
        #------------------------------
        super().__init__(name)
        self.cms_alias = settings.NAME_CMS
        self.cms = get_cms()
        self.emp_alias = settings.NAME_EMP
        self.emp = get_emp()
        self.cms_params = settings.CONFIG.get_PARAMS()

        for key, datos in self.cms_params.items():
            setattr(self, key, datos.get('valor', None))


        self._actions = {
            'delete_selected': admin.actions.delete_selected,
            'delete1_selected': delete1_selected,
            'save1_selected': save1_selected
            }
        self._global_actions = self._actions.copy()
        # all_sites.add(self)
        #-----------------------------------
        try:
            from django.contrib.auth.models import User
            try:
                user_proyecto = User.objects.get(username=settings.PROYECTO)
                print_msg(" 1) Existe Superusuario PROYECTO: %s" % settings.PROYECTO)
            except User.DoesNotExist:
                User.objects.create_superuser(username=settings.PROYECTO,
                        email='mc@multiges.net', password=settings.PROYECTO)
                print_msg(" 1) Crear Superusuario PROYECTO: %s" % settings.PROYECTO)
        except:
            # import pdb; pdb.set_trace()
            if settings.RUNSERVER:
                print_msg(" 0) No hay tablas todavia. Hay que esperar a crear la base de datos")
            return
        #-----------------------
        try:
            user_site = User.objects.get(username=settings.SITE_NAME)   
            print_msg(" 1) Existe Superusuario SITIO: %s" % settings.SITE_NAME)
        except User.DoesNotExist:
            User.objects.create_superuser(username=settings.SITE_NAME,
                    email='mcgaqu@gmail.com', password=settings.SITE_NAME)
            print_msg(" 1) Crear Superusuario SITIO: %s" % settings.SITE_NAME)

        #-----------------------
        site = None
        if settings.SITE_ID:
            from django.contrib.sites.models import Site
            try:
                site = Site.objects.get(pk=settings.SITE_ID)
                if settings.SITE_NAME != site.name:
                    site.name = settings.SITE_NAME
                    site.domain = settings.SITE_DOMAIN or 'www.ainell.es'
                    site.save()

                print_msg(" 3) Existe Site %s: %s" % (site.name, site.domain))
            except Site.DoesNotExist:
                pass
        self.site = site
        #----------

    def get_CmsXs(self):
        if not self.cms:
            return settings.CONFIG.get_CMS_PARAMS()
        else:
            params = cms.datox_set.filter(activo=True)
            dev = {}
            if params:
                for param in params:
                    dev[param.alias] = {'valor': param.valor}
            return dev
       
    def get_CmsX(self, key):
        param = self.CmsXs().get(key, None)
        return None if not param else param.get('valor', None)

    #-----------------------
    def get_rol(self, request):
        obj = request.user
        if not obj.groups.count(): # .count() == 0:
            return None
        else:
            return obj.groups.all()[0]
        
    def registra_modelos(self):
        print_msg("REGISTRAR MODELOS")
        conta = 0
        admins = settings.CONFIG.get_ADMINS()
        for fila in admins:
            try:
                app = import_module("%s.admin" % fila[0])
            except ImportError as exc:
                msg = exc.args[0]
                print_msg("la app %s no tiene admin. %s" % (fila[0], msg))
                continue
            conta +=1
            print_msg("%02d: %s" % (conta, fila))
            if not hasattr(app, fila[1]):
                print_msg("la app %s no tiene el Modelo. %s" % (fila[0], fila[1]))
                import pdb; pdb.set_trace()
            elif not hasattr(app, fila[2]):
                print_msg("la app %s no tiene ModelAadmin. %s" % (fila[0],fila[2]))
                import pdb; pdb.set_trace()
            else:
                self.register(getattr(app, fila[1]), getattr(app, fila[2]))
                    
     
    def each_context(self, request):
        #import pdb; pdb.set_trace() Aquiiiiii pon el arbolnav!
        return {
            **(super().each_context(request)),
            'name_cms': settings.SITE_NAME,
            'name_emp': settings.SITE_NAME,
            'menu_cms': self.menu_list(request)
        }


    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        url1 = [
            # path('ajax/<str:json_alias>/<str:params>/', self.ajax, name='ajax'),
            path('ajax/', self.ajax, name='ajax'),
            path('wp/', self.indexp, name='indexp')
            # path('wp/cliente/', self.indexp, name='indexp_cliente')
            # path('wp/proyecto/', self.indexp, name='indexp_proyecto')
        ]
        return url1 + urls

    def menu_list(self, request):
        #-----------------
        key_session = 'menu_%s_%s' % (request.user.username, settings.SITE_NAME)
        menu_list = request.session.get(key_session, [])
        #-------------------------------------
        # import pdb; pdb.set_trace()
        if not menu_list:
            if request.user.is_superuser:
                return settings.CONFIG.get_menu_super(settings.ROOT_PATH)
            if self.get_rol(request):
                rol_name = self.get_rol(request).name
                roles = settings.CONFIG.get_ROLES(settings.ROOT_PATH)
                if rol_name in roles.keys():
                    menu_list = roles[rol_name][1]
                else:
                    menu_list = []
                # request.session[key_session] = menu_list
                #----------------------------------
                username = request.user.username
                hoy = datetime.date.today()
                sufijo = "?agente1__alias=%s&fecha1__gte=%s" % (username, hoy)
                menu_list.append(
                    [[settings.ROOT_PATH[1:] + 'proyex/hito/%s' % sufijo, 'Hitos Pendientes Vencer'],
                                [ ],
                            ] 
                    )
                #-----------------------
                return menu_list
            else:
                return []


    def get_index_url(self, request):
        index_url = ""
        if self.get_rol(request):
            rol_name = self.get_rol(request).name
            roles_menu_list = settings.CONFIG.get_ROLES(settings.ROOT_PATH)
            if rol_name in roles_menu_list.keys():
                index_url = roles_menu_list[rol_name][0]
        return index_url
    

    def ajax(self, request):
        # import pdb; pdb.set_trace()  
        
        if request.method == "GET":
            data = request.GET
        else:
            data = request.POST
        #---------------
        arco_alias = data.get('funcion', '')
        nombre_arco = arco_alias.split('.')[-1]
        modulo = arco_alias[:-(len(nombre_arco)+1)]
        func_arco = getattr(import_module(modulo), nombre_arco)  
        response = func_arco(request, data) # numero de proyecto
        return response
        #------------------------
        
    
    def index(self, request, extra_context={}):
        extra_context = {
            #'menu_cms': self.menu_list(request),
            'sidebar_items': self.menu_list(request),
            'content_items': self.menu_list(request),
            **(extra_context or {}),
        }
        if self.get_index_url(request):
            return HttpResponseRedirect(self.get_index_url(request))
        return super().index(request, extra_context)


    def login_userx(self, request):
        
        from django.contrib.auth import login
        from django.contrib.auth.models import User, Group
        from mod_entidad.personas.models import Persona
        rol_gestor = Group.objects.get(name="GESTOR")
        rol_admin = Group.objects.get(name="ADMIN")
        usx = request.GET.get('usx', None)
        usx_email = request.GET.get('email', None)
        usx_first_name = request.GET.get('name', None)

        try:
            user = User.objects.get(username=usx)
        except User.DoesNotExist:
            user = User(username=usx)
            user.set_password("_%s" % usx)
            user.email = usx_email
            user.first_name = usx_first_name
            user.is_staff = True
            user.is_active = True
            user.save()
        if not user.groups.all().count():
            if usx in ['JPC2']:
                user.groups.add(rol_admin)
            else:
                user.groups.add(rol_gestor)
            user.save()
            # crear persona
        try:
            persona = Persona.objects.get(alias=usx)
        except Persona.DoesNotExist:
            persona = Persona(alias=usx)
        # persona.entero = int(persona_id)
            persona.nombre = "%s" % usx_first_name
            persona.email = "%s" % usx_email
            persona.activo = True
            persona.de_prod = True
            persona.grupo = "G5"
            persona.user = user
            persona.save()

        clx = request.GET.get('clx', None)
        if clx:
            clx_nombre = request.GET.get('clnombre', None)
            clx_email = request.GET.get('clemail', None)
            try:
                persona = Persona.objects.get(alias=clx)
            except Persona.DoesNotExist:
                persona = Persona(alias=clx)
            # persona.entero = int(persona_id)
                persona.nombre = "%s" % clx_nombre
                persona.email = "%s" % clx_email
                persona.activo = True
                persona.de_venta = True
                persona.grupo = "G5"
                persona.save()
        #-------------------
        # from carga_ini.actions import g5_actualizar
        # g5_actualizar()
        #------------------
        login(request, user)
    
    def indexp(self, request, extra_context={}):
        # import pdb; pdb.set_trace()

        if settings.RUNSERVER:
            # dominio = 'http://cogesa.midns.info:8001'
            dominio ='http://127.0.0.1:8030'
        else:
            dominio ='http://10.101.0.9'
        usx = request.GET.get('usx', None)
        if request.GET.get('usx', None):
            self.login_userx(request)
            if request.GET.get('clx', None):
                clx = request.GET.get('clx', None)
                #----------------------
                from mod_entidad.personas.models import Persona
                try:
                    persona = Persona.objects.get(alias=clx)
                    sufijo = "?cliente=%s&activo=1" % (persona.id)
                except Persona.DoesNotExist:
                    sufijo = ""
                #------------------------
                # sufijo = "?cliente__alias=%s&activo=1" % (clx)
                url = "%sproyex/expdte/%s" % (settings.ROOT_PATH, sufijo)
                #-----------------
                # funcion que actualize el clientes y sus proyectos
                # -------------------------------
                return HttpResponseRedirect(url)
        return self.index(request, extra_context)
    
#--------------------

admin_site1 = AdminSite1(name=settings.SITE_NAME)
"""  
