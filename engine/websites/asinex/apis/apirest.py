# -*- coding: utf-8 -*-

from rest_framework import routers
from mod_auth.adjango.apirest import UserViewSet, GroupViewSet
from mod_auth.companies.apirest import (
    CompanyViewSet, CompanyLoadViewSet, CompanyPropViewSet,
    MenuViewSet, MenuItemViewSet,
)
from mod_auth.doctypes.apirest import DocTypeViewSet, DocTypePropViewSet 
# from mod_core.annexes.apirest import FolderViewSet, FolderAnnexViewSet 



router = routers.DefaultRouter()
#--------------------------------
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
#-------------------
router.register(r'companys', CompanyViewSet)
router.register(r'companyloads', CompanyLoadViewSet)
router.register(r'companyprops', CompanyPropViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'menuitems', MenuItemViewSet)
#-------------------
router.register(r'doctypes', DocTypeViewSet)
router.register(r'doctypeprops', DocTypePropViewSet)
#-------------------
# router.register(r'folders', FolderViewSet)
# router.register(r'folderannexs', FolderAnnexViewSet)
#--------------------------------
