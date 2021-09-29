# -*- coding: utf-8 -*-
import os
from pathlib import Path

SITE_DIR = Path(__file__).resolve(strict=True).parent
SITE_NAME = os.path.basename(SITE_DIR)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost',
        '192.168.1.13', '192.168.0.100', '192.168.0.103',
        '192.168.1.111', '192.168.1.31', '192.168.1.199'
 ] 
 # ALLOWED_HOSTS += get_allowed_hosts()

#------------------
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
 
DATABASE_ROUTERS = [
    'websites.%s.routers.NeodRouter' % SITE_NAME
    # 'mod_admin.routers.UneodRouter', 
    # 'mod_admin.routers.PrimaryReplicaRouter'
]
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
    'rest_framework.authtoken',
    'dj_rest_auth',
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

APPS_NEOD = [
    'neod_auth.empresas.apps.EmpresasConfig',
    'neod_core.clasifclientes.apps.ClasifClientesConfig',
    'neod_core.clasifarticulos.apps.ClasifArticulosConfig',
    'neod_entity.personas.apps.PersonasConfig',
    'neod_entity.productos.apps.ProductosConfig',
    'neod_make.tareas.apps.TareasConfig',
]

INSTALLED_APPS = APPS_INSTALL + APPS_ADMIN
# INSTALLED_APPS += APPS_BPMN
# INSTALLED_APPS += APPS_ERP 
INSTALLED_APPS += APPS_NEOD



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

NEOD_MODELADMINS = [

    ['neod_auth.empresas.apps.EmpresasConfig', [
        ['Empresas1', 'Empresas1Admin1', 1],

    ], ], 
    #-----------------------------------------------
    ['neod_core.clasifclientes.apps.ClasifClientesConfig', [
            ['Zonas1', 'Zonas1Admin1', 1],
            ['SubZonas1', 'SubZonas1Admin1', 1],
    ], ], 
    #--------------------------
    ['neod_core.clasifarticulos.apps.ClasifArticulosConfig', [
            ['Ubicaciones1', 'Ubicaciones1Admin1', 1],
            ['Familias1', 'Familias1Admin1', 1],
            ['Balanzas1', 'Balanzas1Admin1', 1],
            # 4
            ['Marcas1', 'Marcas1Admin1', 1],
            ['Modelos1', 'Modelos1Admin1', 1],
            ['Origen1', 'Origen1Admin1', 1],
            # 7
            ['Tallas1', 'Tallas1Admin1', 1],
            ['Colores1', 'Colores1Admin1', 1],
            ['TiposMateria1', 'TiposMateria1Admin1', 1],
            ['TarifaCab1', 'TarifaCab1Admin1', 1],
            ['MargenesCab1', 'MargenesCab1Admin1', 1],
            ['MargenesDet1', 'MargenesDet1Admin1', 1],
    ], ], 
    #-----------------------------------------------	
    ['neod_entity.personas.apps.PersonasConfig', [
            ['Tecnicos1', 'Tecnicos1Admin1', 1],
            ['Clientes1', 'Clientes1Admin1', 1],
            ['ClientesContacto1', 'ClientesContacto1Admin1', 1],
            ['Proveedores1', 'Proveedores1Admin1', 1],
            ['Acreedores1', 'Acreedores1Admin1', 1],
            ['Usuarios1', 'Usuarios1Admin1', 1],
            ['UsuarioWeb1', 'UsuarioWeb1Admin1', 1],
    ], ],   
    #-----------------------------------------------	
    ['neod_entity.productos.apps.ProductosConfig', [
            ['Articulos1', 'Articulos1Admin1', 1],
            ['ArtiProveedor1', 'ArtiProveedor1Admin1', 1],
            ['Formatos1', 'Formatos1Admin1', 1],
            ['TarifaDet1', 'TarifaDet1Admin1', 1],
            ['CabProvTarifas1', 'CabProvTarifas1Admin1', 1],
            ['DetProvTarifas1', 'DetProvTarifas1Admin1', 1],
            ['Disponibilidad1', 'Disponibilidad1Admin1', 1],
    ], ],
    #-----------------------------------------------	
    ['neod_make.tareas.apps.TasreasConfig', [
            ['TipoAccion1', 'TipoAccion1Admin1', 1],
            ['TipoTareas1', 'TipoTareas1Admin1', 1],
            ['Tareas1', 'Tareas1Admin1', 1],
            ['Acciones1', 'Acciones1Admin1', 1],
 
    ], ],

    #-----------------------------------------------	
    # ['neod_entity.ndprojects.apps.NdProjectsConfig', [
    #         ['CabVentas1', 'CabVentas1Admin1', 1],
    # ], ],

]




MODELADMINS = [] # AUTH_MODELADMINS
# MODELADMINS +=  BPMN_MODELADMINS 
# MODELADMINS +=  CORE_MODELADMINS
# MODELADMINS +=  ENTITY_MODELADMINS
# MODELADMINS +=  MAKE_MODELADMINS
# MODELADMINS +=  ORDER_MODELADMINS
MODELADMINS +=  NEOD_MODELADMINS

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
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
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


