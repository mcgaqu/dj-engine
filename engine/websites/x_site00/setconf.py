# -*- coding: utf-8 -*-
import os
from pathlib import Path

SITE_DIR = Path(__file__).resolve(strict=True).parent
SITE_NAME = os.path.basename(SITE_DIR)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost',
        '192.168.1.29', '192.168.0.107'
 ] 
 # ALLOWED_HOSTS += get_allowed_hosts()

#------------------
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
 
# DATABASE_ROUTERS = [
#     'mod_admin.routers.UneodRouter', 
#     # 'mod_admin.routers.PrimaryReplicaRouter'
# ]
#------------------------------

MIDDLEWARE = [
    #------------------
    'corsheaders.middleware.CorsMiddleware',
    #---------------------
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.admindocs.middleware.XViewMiddleware',
]

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
    #--------------------------
    'django_filters',
    'rest_framework',
    #---------------------

    # 'rest_framework.authtoken',
    'corsheaders',
    'markdown',
    # 'pygments'
    #----------------------
    # 'graphene_django',
    #------------------

] 

APPS_ADMIN = [
    'firebird.apps.FirebirdConfig',
    
    #------------------        
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
    'mod_entity.persons.apps.PersonsConfig',
    'mod_entity.products.apps.ProductsConfig',
    'mod_entity.projects.apps.ProjectsConfig',
    'mod_make.tasks.apps.TasksConfig',
    'mod_make.works.apps.WorksConfig',
    'mod_order.commands.apps.CommandsConfig',
    'mod_order.invoices.apps.InvoicesConfig',
    # mod_order.payment.apps.PaymentsConfig'
]

INSTALLED_APPS = APPS_INSTALL + APPS_ADMIN
INSTALLED_APPS += APPS_BPMN
INSTALLED_APPS += APPS_ERP 
# INSTALLED_APPS += APPS_NEOD



#-------------------------
# Modeladmins
#---------------------------------

AUTH_MODELADMINS = [
    ['mod_auth.adjango.apps.AdjangoConfig', [
            ['ContentType', 'ContentTypeAdmin1', 1],     
            ['Permission', 'PermissionAdmin1', 1],
            ['User', 'UserAdmin1', 1],     
            ['Group', 'GroupAdmin1', 1],
            ['LogEntry', 'LogEntryAdmin1', 1],
            ['Session', 'SessionAdmin1', 1],        
     ], ],
    ['mod_auth.companies.apps.CompaniesConfig', [
            ['Company', 'CompanyAdmin1', 2],
            ['CompanyProp', 'CompanyPropAdmin1', 1],
            ['CompanyLoad', 'CompanyLoadAdmin1', 1],
            ['Menu', 'MenuAdmin1', 1],
            ['MenuItem', 'MenuItemAdmin1', 2],
        ],
    ],
    #---------------------------------------
    ['mod_auth.doctypes.apps.DocTypesConfig', [
            ['DocType', 'DocTypeAdmin1', 2],
            ['DocTypeProp', 'DocTypePropAdmin1', 1],
     ], ],

] 


BPMN_MODELADMINS = [
    ['mod_bpmn.business.apps.BusinessConfig', [
            ['Biz', 'BizAdmin1', 1],
     ], ],            
    ['mod_bpmn.data.apps.DataConfig', [
            ['BApp', 'BAppAdmin1', 1],
            ['BModel', 'BModelAdmin1', 1],
            ['BModelField', 'BModelFieldAdmin1', 1],
            ['BModelAction', 'BModelActionAdmin1', 1],
     ], ],
    #-----------------------------------------------	
    ['mod_bpmn.datastate.apps.DatastateConfig', [
            ['BAction', 'BActionAdmin1', 1],
            ['BReducer', 'BReducerAdmin1', 1],
            ['BStore', 'BStoreAdmin1', 1],
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
    # #-----------------------------------------------	
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

CORE_MODELADMINS = [

    ['mod_core.annexes.apps.AnnexesConfig', [
            ['Folder', 'FolderAdmin1', 2],
            ['FolderAnnex', 'FolderAnnexAdmin1', 1],
     ], ],
]

ENTITY_MODELADMINS = [
    ['mod_entity.persons.apps.PersonsConfig', [
            ['Segment', 'SegmentAdmin1', 1],
            ['Person', 'PersonAdmin1', 1],
            ['PersonAux', 'PersonAuxAdmin1', 1],
            ['Customer', 'CustomerAdmin1', 1],
            # ['NeodCliente', 'NeodClienteAdmin1', 1],
            # ['NeodClienteContacto', 'NeodClienteContactoAdmin1', 1],
                        # ['PersonItem', 'PersonItemAdmin1', 1],
        ],
    ],
    #-----------------------------------------------	
    ['mod_entity.products.apps.ProductsConfig', [
            ['Category', 'CategoryAdmin1', 1],
            ['Product', 'ProductAdmin1', 2],
            ['ProductAux', 'ProductAuxAdmin1', 2],
            # ['ProductItem', 'ProductItemAdmin1', 1],
        ],
    ],
    #-----------------------------------------------	
    ['mod_entity.projects.apps.ProjectsConfig', [
            ['Project', 'ProjectAdmin1', 1],
            ['Expedient', 'ExpedientAdmin1', 2],
            ['ExpedientAux', 'ExpedientAuxAdmin1', 2],
        ],
    ],
]

MAKE_MODELADMINS = [
    ['mod_make.tasks.apps.TasksConfig', [
            ['Task', 'TaskAdmin1', 2],
            ['TaskAux', 'TaskAuxAdmin1', 1],
        ],
    ],
    #-----------------------------------------------	
    ['mod_make.works.apps.WorksConfig', [
            ['Work', 'WorkAdmin1', 2],
            ['WorkAux', 'WorkAuxAdmin1', 1],
        ],
    ],
]

ORDER_MODELADMINS = [
    #-----------------------------------------------	
    ['mod_order.commands.apps.CommandsConfig', [
            ['Command', 'CommandAdmin1', 2],
            ['CommandAux', 'CommandAuxAdmin1', 1],
        ],
    ],
    #-----------------------------------------------	
    ['mod_order.invoices.apps.CommandsConfig', [
            ['Invoice', 'InvoiceAdmin1', 2],
            ['InvoiceAux', 'InvoiceAuxAdmin1', 1],
        ],
    ],
    #-----------------------------------------------	
    # ['mod_order.payments.apps.PaymentsConfig', [
    #         ['Payment', 'PaymentAdmin1', 2],
    #         ['PaymentAux', 'PaymentAuxAdmin1', 1],
    #     ],
    # ],

]


MODELADMINS = AUTH_MODELADMINS
MODELADMINS +=  BPMN_MODELADMINS 
MODELADMINS +=  CORE_MODELADMINS
MODELADMINS +=  ENTITY_MODELADMINS
MODELADMINS +=  MAKE_MODELADMINS
MODELADMINS +=  ORDER_MODELADMINS

#====================
# APIS
#---------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'mod_admin.main1.restapi.PageNumberPagination1',
    'PAGE_SIZE': 20,
    #-----------------
    'DEFAULT_FILTER_BACKENDS': [
        # 'rest_framework.filters.DjangoFilterBackend',
        # 'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # 'ORDERING_PARAM' : 'ordering',
    # 'SEARCH_PARAM' : 'search',
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://192.168.1.19:3000",
]
#------------------------------------------
# ojo!!! hay que crear SCHEMA_OUTPUT desde SCHEMA
# mapage.py graphql_schema --schema engine.schema.schema --out engine.data_schema.json

GRAPHENE = {
    'SCHEMA': '%s.apigrql.schema' % SITE_NAME, # Where your Graphene schema lives
    'SCHEMA_OUTPUT': '%s.data_schema.json' % SITE_NAME,
    'SCHEMA_INDENT': 4,
    # 'MIDDLEWARE': 'graphene_django.debug.DjangoDebugMiddleware',
}

#==============================


