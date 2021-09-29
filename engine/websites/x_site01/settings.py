# -*- coding: utf-8 -*-
import os
from pathlib import Path

from .setconf import   (ALLOWED_HOSTS,
                        LANGUAGE_CODE, TIME_ZONE,
                        # DATA_ROOT,
                        # DATABASES, DB_CONFIG, SITE_ID,
                        # DATABASE_ROUTERS,
                        MIDDLEWARE, 
                        INSTALLED_APPS,
                        MODELADMINS,
                        REST_FRAMEWORK,
                        # CORS_ALLOWED_ORIGINS,
                        CORS_ALLOW_ALL_ORIGINS,
                        GRAPHENE,
                        )                    
#=========================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+mg*=m_9!n3$l+gg8)*4k&a33zzo7_blbid4j#h6^1xg=1x8g2'

# SECURITY WARNING: don't run with debug turned on in production!

#================================
# GENERAL
#==========================
SITE_DIR = Path(__file__).resolve(strict=True).parent
SITE_NAME = os.path.basename(SITE_DIR)
if os.path.basename(SITE_DIR) == "websites":
    BASE_DIR = SITE_DIR.parent.parent
else:
    BASE_DIR = SITE_DIR.parent
BASE_NAME = os.path.basename(BASE_DIR) # ymaker


USER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
# user_dir = 'home/%s' % USER_NAME
USER_NAME = os.path.basename(USER_DIR)
#------------------
# NUM_ADMIN_SITE = "0" # ("0" = prototype-django, "1" = dev, "2" = production)  se podria obtener del environ
NUM_ADMIN_SITE = os.environ.get('NUM_ADMIN_SITE', "0")

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

# ROOT_PATH = "/%s/" % (SITE_NAME)

# DATA_ROOT = os.path.join(os.path.dirname(
# 				os.path.dirname(BASE_DIR)), 'SITES_DATOS', SITE_NAME)
DATA_ROOT = os.path.join(BASE_DIR.parent.parent, 'SITES_DATOS', SITE_NAME)
#----------------------------------
#=======================================
# DATABASES
#========================================
# db_dir = Path(__file__).resolve(strict=True).parent
db_dir = DATA_ROOT
db_name = os.path.basename(db_dir)
db_name_main = 'LOYPAR_GES'

db_name_firebird = 'C:\\Unita_bases\LOYPAR_GES.FDB'
host_firebird = '192.168.43.8'
port_firebird = '3051'
# fb_library_name = 'C:\\ProgramFiles\Firebird'     # Windows
fb_library_name = '/Library/Frameworks/Firebird.framework/Resources/bin/firebird'  # Apple

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(db_dir, '%s.sqlite3' % db_name), 
    },
    # 'main': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(db_dir, '%s.sqlite3' % db_name_main), 
    # },
    'firebird1': {
        'ENGINE' : 'firebird',
        'NAME': db_name_firebird, # Path to database or db alias
        'USER': 'SYSDBA',           # Your db user
        'PASSWORD': 'masterkey',    # db user password
        'HOST': host_firebird,        # Your host machine
        'PORT': port_firebird,             # If is empty, use default 3050
        'OPTIONS' : {
            'charset':'ISO8859_1', 
            'fb_library_name': fb_library_name 
        }
    }

}
# import pdb; pdb.set_trace()

# x_DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'wmk_%s' % db_name,
#         'USER': 'wmk_%s' % db_name,
#         'PASSWORD': '%s_mk' % db_name,
#         'HOST': '',
#         'PORT': ''
#     }

# x_DATABASES = {
#     'default': {
#         'ENGINE' : 'firebird',
#         'NAME' : '/var/lib/firebird/2.5/data/django_firebird.fdb', # Path to database or db alias
#         'USER' : 'SYSDBA',           # Your db user
#         'PASSWORD' : '*****',    # db user password
#         'HOST' : '127.0.0.1',        # Your host machine
#         'PORT' : '3050',             # If is empty, use default 3050
#         #'OPTIONS' : {'charset':'ISO8859_1'}
#     }
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
#------------------------------
DB_CONFIG = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(db_dir, 'db.sqlite3'), 
    }
DB_CONFIG = DATABASES['default']

SITE_ID = 1
#============================
# Application definition


ROOT_URLCONF = 'websites.%s.urls' % SITE_NAME
WSGI_APPLICATION = 'websites.%s.wsgi.application' % SITE_NAME


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

#--------------------------
# STATICFILES
#-----------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/%s/static/' % SITE_NAME
STATIC_ROOT = '%s/' % os.path.join(# os.path.dirname(
    os.path.dirname(BASE_DIR), # ),
    '%s_static' % (SITE_NAME.lower()))

#------------------------------
# MEDIA FILES
#-----------------------

MEDIA_URL = '/%s/media/' % SITE_NAME
MEDIA_ROOT = '%s/' % os.path.join( # os.path.dirname(
    os.path.dirname(BASE_DIR), #),
    '%s_media'% (SITE_NAME.lower()))

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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

#--------------------------
# I18n
#----------------------------

# https://docs.djangoproject.com/en/dev/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# import pdb; pdb.set_trace()
