# -*- coding: utf-8 -*-
import os
from pathlib import Path

#=================================
# INSTALLED_APPS
#===================================
APPS_INSTALL = [
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites.apps.SitesConfig',
    #---------------------
    'ckeditor',
    'ckeditor_uploader',
    #--------------------------
    'django_filters',
    #---------------------
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'markdown',
    #----------------------
    'graphene_django',
    #------------------
    'xlrd', 'xlwt',
    'django_docutils',
] 

APPS_ADMIN = [ 
    'mod_admin.main1.apps.Main1Config',
    'mod_admin.main2.apps.Main2Config',
    'mod_admin.models',
    #--------------------
    'mod_auth.adjango.apps.AdjangoConfig',
    'mod_auth.companies.apps.CompaniesConfig',
    'mod_auth.doctypes.apps.DocTypesConfig',
    #-------------------------
]

APPS_BPMN = [
    'mod_bpmn.business.apps.BusinessConfig',
    'mod_bpmn.data.apps.DataConfig',
    'mod_bpmn.datastate.apps.DatastateConfig',    
    'mod_bpmn.layouts.apps.LayoutsConfig',
    'mod_bpmn.mdas.apps.MdasConfig',    
    #------------------------------------
    # 'mod_bpmn.cocklists.apps.CocklistsConfig',
    # 'mod_bpmn.tasklists.apps.TasklistsConfig', 
    #------------------------
]

APPS_ERP = [
    'mod_core.annexes.apps.AnnexesConfig', 
    # 'mod_core.kinds.apps.KindsConfig',  
    # 'mod_entity.persons.apps.PersonsConfig',
    # 'mod_entity.products.apps.ProductsConfig',
    # 'mod_entity.projects.apps.ProjectsConfig',
    #--------------
    # 'mod_make.plans.apps.PlansConfig',

    # 'mod_make.tasks.apps.TasksConfig',
    # 'mod_make.works.apps.WorksConfig',
    #--------------
    
    # 'mod_order.commands.apps.CommandsConfig',
    # 'mod_order.deliveries.apps.DeliveriesConfig',  
    # 'mod_order.invoices.apps.InvoicesConfig',
    # 'mod_order.payments.apps.PaymentesConfig', 
    #-------------   
    # 'websites.asinex.config',
]

INSTALLED_APPS = APPS_INSTALL + APPS_ADMIN
# INSTALLED_APPS += APPS_BPMN
INSTALLED_APPS += APPS_ERP 

#=======================

BPMN_MODELADMINS = [
    ['mod_bpmn.business.apps.BusinessConfig', [
            ['Biz', 'BizAdmin1', 1],
     ], ],
    # #-----------------------------------------------
    ['mod_bpmn.data.apps.DataConfig', [
            ['BApp', 'BAppAdmin1', 1],
            ['BModel', 'BModelAdmin1', 1],
            ['BModelField', 'BModelFieldAdmin1', 1],
            ['BModelAction', 'BModelActionAdmin1', 1],
     ], ],
    # #-----------------------------------------------		
    ['mod_bpmn.datastate.apps.DatastateConfig', [
            ['BAction', 'BActionAdmin1', 1],
            ['BReducer', 'BReducerAdmin1', 1],
            ['Plantore', 'PlantoreAdmin1', 1],
     ], ],

    #---------------------------------------
    ['mod_bpmn.layouts.apps.LayoutsConfig', [
            ['Component', 'ComponentAdmin1', 1],
            ['CompProp', 'CompPropAdmin1', 1],
            ['Layout', 'LayoutAdmin1', 1],
     ], ],

    #--------------------------------
    ['mod_bpmn.mdas.apps.MdasConfig', [
            ['Mda', 'MdaAdmin1', 1],
            ['MdaAux', 'MdaAuxAdmin1', 1],
            ['MdaView', 'MdaViewAdmin1', 1],
            ['MdaViewAux', 'MdaViewAuxAdmin1', 1],
     ], ],
    #-----------------------------------------------	
    #--------------------------------
    # ['mod_base.state.apps.DatastateConfig', [

    #  ], ],

    #--------------------------------- 
    # ['mod_bpmn.datastate.apps.DatastateConfig', [

    #  ], ],
    #--------------------------------
    # ['mod_bpmn.tasklist.apps.StateConfig', [

    #  ], ],
    #-----------------------------------------------
]
#-------------------------
# Modeladmins
#---------------------------------

x_MODELADMINS = [
    ['mod_auth.adjango.apps.AdjangoConfig', [
            ['ContentType', 'ContentTypeAdmin1', 1],     
            ['Permission', 'PermissionAdmin1', 1],
            ['User', 'UserAdmin1', 1],     
            ['Group', 'GroupAdmin1', 1],
            ['LogEntry', 'LogEntryAdmin1', 1],
            ['Session', 'SessionAdmin1', 1], 
            ['Site', 'SiteAdmin1', 1],        
     ], ],
    ['mod_auth.companies.apps.CompaniesConfig', [
            ['Company', 'CompanyAdmin1', 2],
            ['CompanyLoad', 'CompanyLoadAdmin1', 1],
            ['CompanyProp', 'CompanyPropAdmin1', 1],
            ['Menu', 'MenuAdmin1', 1],
            ['MenuItem', 'MenuItemAdmin1', 2],
        ],
    ],
    #---------------------------------------
    ['mod_auth.doctypes.apps.CompaniesConfig', [
            ['DocType', 'DocTypeAdmin1', 2],
            ['DocTypeProp', 'DocTypePropAdmin1', 1],
     ], ],

] + [ # BPMN_MODELADMINS + [

    ['mod_core.annexes.apps.AnnexesConfig', [
            ['Folder', 'FolderAdmin1', 2],
            ['FolderAnnex', 'FolderAnnexAdmin1', 1],
     ], ],
    ['mod_core.kinds.apps.KindsConfig', [
            ['Kind', 'KindAdmin1', 2],
            ['KindAux', 'KindAuxAdmin1', 1],
     ], ],
    #--------------------------------
    ['mod_entity.persons.apps.PersonsConfig', [
            ['Person', 'PersonAdmin1', 1],
            ['PersonAux', 'PersonAuxAdmin1', 1],
            # ['PersonItem', 'PersonItemAdmin1', 1],
    ], ],
    #-----------------------------------------------	
    ['mod_entity.products.apps.ProductsConfig', [
            ['Product', 'ProductAdmin1', 2],
            ['ProductAux', 'ProductAuxAdmin1', 2],
            # ['ProductItem', 'ProductItemAdmin1', 1],
    ],],
    #-----------------------------------------------	
    ['mod_make.plans.apps.PlansConfig', [
            ['Plan', 'PlanAdmin1', 2],
            ['PlanFactor', 'PlanFactorAdmin1', 2],
            ['PlanFactorAux', 'PlanFactorAuxAdmin1', 2],

            #-----------
            ['PlanDoc', 'PlanDocAdmin1', 2],
            ['PlanDocProduct', 'PlanDocProductAdmin1', 2],
            ['PlanDocTax', 'PlanDocTaxAdmin1', 2],
            #--------------
            # ['Company', 'PlanCompanyAdmin1', 2],
            # ['Person', 'PlanPersonAdmin1', 2],
            # ['Product', 'PlanProductAdmin1', 2],
    ],],
#     ['mod_make.projects.apps.ProjectsConfig', [
#             ['Project', 'ProjectAdmin1', 2],
#             ['ProjectAux', 'ProjectAuxAdmin1', 2],
#             # ['ProjectItem', 'ProjectItemAdmin1', 1],
#     ],],
#     ['mod_make.tasks.apps.TasksConfig', [
#             ['Task', 'TaskAdmin1', 2],
#             ['TaskAux', 'TaskAuxAdmin1', 2],
#     ],],
#     ['mod_make.works.apps.WorksConfig', [
#             ['Work', 'WorkAdmin1', 2],
#             ['WorkAux', 'WorkAuxAdmin1', 2],
#     ],],
    #-----------------------------------------------	

    #-----------------------------------------------	

]

MODELADMINS = [
    ['mod_auth.adjango.apps.AdjangoConfig', [
            ['ContentType', 'ContentTypeAdmin1', 1],     
            ['Permission', 'PermissionAdmin1', 1],
            ['User', 'UserAdmin1', 1],     
            ['Group', 'GroupAdmin1', 1],
            ['LogEntry', 'LogEntryAdmin1', 1],
            ['Session', 'SessionAdmin1', 1], 
            ['Site', 'SiteAdmin1', 1],        
     ], ],
    ['mod_auth.companies.apps.CompaniesConfig', [
            ['Company', 'CompanyAdmin1', 2],
            ['CompanyLoad', 'CompanyLoadAdmin1', 1],
            ['CompanyProp', 'CompanyPropAdmin1', 1],
            ['Menu', 'MenuAdmin1', 1],
            ['MenuItem', 'MenuItemAdmin1', 2],
        ],
    ],
    #---------------------------------------
    ['mod_auth.doctypes.apps.CompaniesConfig', [
            ['DocType', 'DocTypeAdmin1', 2],
            ['DocTypeProp', 'DocTypePropAdmin1', 1],
     ], ],

] + [ # BPMN_MODELADMINS + [

    ['mod_core.annexes.apps.AnnexesConfig', [
            ['Folder', 'FolderAdmin1', 2],
            ['FolderAnnex', 'FolderAnnexAdmin1', 1],
    ], ],
    # ['mod_core.kinds.apps.KindsConfig', [
    #         ['Kind', 'KindAdmin1', 2],
    #         ['KindAux', 'KindAuxAdmin1', 1],
    #  ], ],
    #--------------------------------
    # ['mod_entity.persons.apps.PersonsConfig', [
    #         ['Person', 'PersonAdmin1', 1],
    #         # ['PersonAux', 'PersonAuxAdmin1', 1],
    #         # ['PersonItem', 'PersonItemAdmin1', 1],
    # ], ],
    # #-----------------------------------------------	
    # ['mod_entity.products.apps.ProductsConfig', [
    #         ['Product', 'ProductAdmin1', 2],
    #         # ['ProductAux', 'ProductAuxAdmin1', 2],
    #         # ['ProductItem', 'ProductItemAdmin1', 1],
    # ],],
    # #-----------------------------------------------	
    # ['mod_entity.projects.apps.ProjectsConfig', [
    #         ['Project', 'ProjectAdmin1', 2],
    #         # ['ProductAux', 'ProductAuxAdmin1', 2],
    #         # ['ProductItem', 'ProductItemAdmin1', 1],
    # ],],
    # #-----------------------------------------------	

]


def get_param_settings(param, default=None):
    PARAMS = {
        'SECRET_KEY' : '+mg*=m_9!n3$l+gg8)*4k&a33zzo7_blbid4j#h6^1xg=1x8g2',
        'ALLOWED_HOSTS' : ['127.0.0.1', 'localhost', '192.168.0.107'], 
        #------
        'LANGUAGE_CODE' : 'es-es',
        'TIME_ZONE' : 'UTC',
        'USE_I18N' : True,
        'USE_L10N' : True,
        'USE_TZ' : True,
        #--------
        # 'MIDDLEWARE': '',
        # 'TEMPLATES': '',
        # 'AUTH_PASSWORD_VALIDATORS': '',
        # #------------
        # 'DATA_ROOT': '',
        # 'DATABASES': '', 
        # 'SITE_ID': 1,
        # 'DATABASE_ROUTERS': '',
        # #-----
        # 'STATIC_URL': '',
        # 'STATIC_ROOT': '',
        # 'MEDIA_URL': '',
        # 'MEDIA_ROOT': '',
        # #---
        # 'REST_FRAMEWORK':'',
        # 'CORS_ALLOW_ALL_ORIGINS': '',
        # 'GRAPHENE': '',
        #----------
        'SITE_ID': 1,
        'COMPANY_ID': 1,
        'BIZ_ID': 0,
        'INSTALLED_APPS': INSTALLED_APPS,
        'MODELADMINS': MODELADMINS ,
        #------
    }

    if not param in PARAMS.keys():
        return default
    return PARAMS[param]
    