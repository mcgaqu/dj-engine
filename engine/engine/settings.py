# -*- coding: utf-8 -*-
import os
from pathlib import Path

from .config.setconf import get_param_settings

#================================
# 0. GENERAL: PARAMETROS FIJOS
#==========================
SITE_DIR = Path(__file__).resolve(strict=True).parent
SITE_NAME = os.path.basename(SITE_DIR)
if os.path.basename(SITE_DIR.parent) == "websites":
    BASE_DIR = SITE_DIR.parent.parent
    SITE_NAMEX = 'websites.%s' % (SITE_NAME)

else:
    BASE_DIR = SITE_DIR.parent
    SITE_NAMEX = SITE_NAME


BASE_NAME = os.path.basename(BASE_DIR) # ymaker

USER_DIR = BASE_DIR.parent.parent.parent
USER_NAME = os.path.basename(USER_DIR)

RUNSERVER = os.environ.get('RUNSERVER', False)
if RUNSERVER or SITE_NAME == BASE_NAME: # zrun con WSGI
    DEBUG = True
    PREFIX_URL = '%s/' % SITE_NAME
else: # apache 
    DEBUG = False
    PREFIX_URL = '' 
# import pdb; pdb.set_trace()
# DEBUG = False if NUM_ADMIN_SITE == 2 else True
#---------------------------
NUM_ADMIN_SITE = os.environ.get('NUM_ADMIN_SITE', "1")

#=======================================
# 1. APLICACION
#========================================
ROOT_URLCONF = '%s.urls' % SITE_NAMEX
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAMEX   

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "mod_admin/main1/templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



#=======================================
# 2. DATABASES AND FILES
#========================================
DATA_ROOT = os.path.join(BASE_DIR.parent.parent, 'SITES_DATOS', SITE_NAME)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_ROOT, '%s.sqlite3' % SITE_NAME), 
    },
}

DATABASE_ROUTERS = []

STATIC_URL = '/%s/static/' % SITE_NAME
# STATIC_URL = '/static/'
STATIC_ROOT = '%s/' % os.path.join(DATA_ROOT ,'%s_static' % SITE_NAME.lower())
MEDIA_URL = '/%s/media/' % SITE_NAME
# MEDIA_URL = '/media/'
MEDIA_ROOT = '%s/' % os.path.join(DATA_ROOT ,'%s_media' % SITE_NAME.lower())

# CKEDITOR_BASEPATH = "/my_static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

#====================
# APIS
#===================

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.TokenAuthentication',
    # ),
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'mod_admin.main1.restapi.PageNumberPagination1',
    'PAGE_SIZE': 100,
    #-----------------
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'rest_framework.filters.OrderingFilter',
        
    ],
    'ORDERING_PARAM' : 'ordering',
    'SEARCH_PARAM' : 'search',
}

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:3000",
#     "http://localhost:3000",
#     "http://localhost:58930",
#     "http://127.0.0.1:58930",
#     'http://localhost:49381',
# ]
#------------------------------------------


GRAPHENE = {
    # ojo!!! hay que crear SCHEMA_OUTPUT desde SCHEMA
    # mapage.py graphql_schema --schema [SITE_NAMEX].schema.schema --out [SITE_NAMEX].data_schema.json
    'SCHEMA': '%s.apis.apigrql.schema' % SITE_NAMEX, # Where your Graphene schema lives
    'SCHEMA_OUTPUT': '%s.data_schema.json' % SITE_NAMEX,
    'SCHEMA_INDENT': 4,
    # 'MIDDLEWARE': 'graphene_django.debug.DjangoDebugMiddleware',
}




#================================
# SETCONF
#==========================
SECRET_KEY = get_param_settings('SECRET_KEY', '+mg*=m_9!n3$l+gg8)*4k&a33zzo7_blbid4j#h6^1xg=1x8g2')
ALLOWED_HOSTS = get_param_settings('ALLOWED_HOSTS', ['127.0.0.1', 'localhost', '192.168.1.19']) 
#------
LANGUAGE_CODE = get_param_settings('LANGUAGE_CODE' , 'es-es')
TIME_ZONE = get_param_settings( 'TIME_ZONE' , 'UTC')
USE_I18N = get_param_settings('USE_I18N' , True)
USE_L10N = get_param_settings('USE_L10N' , True)
USE_TZ = get_param_settings('USE_TZ' , True)
#--------
MIDDLEWARE = get_param_settings('MIDDLEWARE', MIDDLEWARE)
TEMPLATES = get_param_settings('TEMPLATES', TEMPLATES)
AUTH_PASSWORD_VALIDATORS = get_param_settings('AUTH_PASSWORD_VALIDATORS', AUTH_PASSWORD_VALIDATORS)
#---
DATA_ROOT = get_param_settings('DATA_ROOT', DATA_ROOT)
DATABASES = get_param_settings('DATABASES', DATABASES) 

DATABASE_ROUTERS = get_param_settings('DATABASE_ROUTERS', DATABASE_ROUTERS)
#------
STATIC_URL = get_param_settings('STATIC_URL', STATIC_URL)   
STATIC_ROOT = get_param_settings('STATIC_ROOT', STATIC_ROOT)  
MEDIA_URL = get_param_settings('STATIC_URL', MEDIA_URL)   
MEDIA_ROOT = get_param_settings('STATIC_ROOT', MEDIA_ROOT) 
#--- 
REST_FRAMEWORK = get_param_settings('REST_FRAMEWORK', REST_FRAMEWORK) 
CORS_ALLOW_ALL_ORIGINS  = get_param_settings('CORS_ALLOW_ALL_ORIGINS ', CORS_ALLOW_ALL_ORIGINS) 
GRAPHENE = get_param_settings('GRAPHENE', GRAPHENE) 
#---------
SITE_ID = get_param_settings('SITE_ID', 1)
COMPANY_ID = get_param_settings('COMPANY_ID', SITE_ID)
BIZ_ID = get_param_settings('BIZ_ID', 0)
INSTALLED_APPS = get_param_settings('INSTALLED_APPS')
MODELADMINS = get_param_settings('MODELADMINS')
#------


# import pdb; pdb.set_trace()
#==============================


