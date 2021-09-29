#!/usr/bin/env python

"""engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from importlib import import_module
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
# from graphene_django.views import GraphQLView
from rest_framework.authtoken import views

# from .apigrql import schema
from .apirest import router

# from .config import  SITE_NAME, PREFIX_URL, RUNSERVER, NUM_ADMIN_SITE
# import pdb; pdb.set_trace()

num_admin_site = settings.NUM_ADMIN_SITE
if num_admin_site == "0" :
    #-----------------------
    # admin de django
    #------------------------
    # admin_site_activo = admin.site
    admin.autodiscover()
    # prefix = ""
    admin_site_activo = admin.site
else:
    from .sites import AdminSite
    admin_site_activo = AdminSite(name=settings.SITE_NAME)
    admin_site_activo.register_models()


prefix = settings.PREFIX_URL

urlpatterns = [
    # path('%sadmin/doc/' % prefix, include('django.contrib.admindocs.urls')),
    # path('%sadmin/' % prefix, admin.site.urls),
    #--------------------------
    # path('%s/doc/' % prefix, include('django.contrib.admindocs.urls')),
    path('%sadmin/doc/' % prefix, include('django.contrib.admindocs.urls')),
    path('%sapirest/' % prefix, include(router.urls)),
    path('%sdj-rest-auth/' % prefix, include('dj_rest_auth.urls')),
    path('%sapi-token-auth/' % prefix, views.obtain_auth_token),
    # path('%sapigrql/' % prefix, csrf_exempt(GraphQLView.as_view(
    #     graphiql=True,  schema=schema))),
    path(prefix, admin_site_activo.urls),

]

# urlpatterns = [
#     path('dj-rest-auth/', include('dj_rest_auth.urls')),
# ]
if settings.RUNSERVER:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
