# -*- coding: utf-8 -*-

from rest_framework import routers
from mod_auth.adjango.apirest import UserViewSet, GroupViewSet
# from mod_auth.business.apirest import BizViewSet, CompanyViewSet, CompanyAuxViewSet
# from mod_base.layouts.apirest import ComponentViewSet, CompPropViewSet

# from mod_base.components.apirest import CmsViewSet, ComponentViewSet, ElementViewSet
# from mod_base.designs.apirest import WebSetViewSet, WebSetElementViewSet

# from mod_engine.companies.apirest import (
#     CompanyViewSet, CategoryViewSet,
#     CompanyAuxViewSet, CategoryAuxViewSet,
# )
# from mod_entity.contacts.apirest import ContactViewSet, ContactAuxViewSet 
# from mod_entity.products.apirest import ProductViewSet, ProductAuxViewSet 
# from mod_entity.projects.apirest import ProjectViewSet, ProjectAuxViewSet 
# from mod_event.jobs.apirest import JobViewSet
# from mod_event.posts.apirest import PostViewSet
# from mod_event.tasks.apirest import TaskViewSet

# from mod_order.commands.apirest import CommandViewSet,  CommandProductViewSet
# from mod_order.invoices.apirest import InvoiceViewSet,  InvoiceCommandViewSet
# from mod_order.payments.apirest import PaymentViewSet,  PaymentInvoiceViewSet

from rest_framework.pagination import PageNumberPagination

class PageNumberPagination1(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 10000


router = routers.DefaultRouter()
#--------------------------------
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
#-------------------
# router.register(r'bizs', BizViewSet)

# router.register(r'companys', CompanyViewSet)
# router.register(r'companyauxs', CompanyAuxViewSet)
#--------------------------------
# router.register(r'components', ComponentViewSet)
# router.register(r'compprops', CompPropViewSet)
#--------------------------------

#----------------------------------
# router.register(r'contact', ContactViewSet)
# router.register(r'contactaux', ContactAuxViewSet)
# #---------------------------------
# router.register(r'product', ProductViewSet)
# router.register(r'productaux', ProductAuxViewSet)
# #---------------------------------
# router.register(r'project', ProjectViewSet)
# router.register(r'projectaux', ProjectAuxViewSet)
# #---------------------------------
# router.register(r'job', JobViewSet)
# router.register(r'post',PostViewSet)
# router.register(r'task', TaskViewSet)
# #---------------------------------
# router.register(r'command',CommandViewSet)
# router.register(r'commandproduct', CommandProductViewSet)
# #---------------------------------
# router.register(r'invoice',InvoiceViewSet)
# router.register(r'invoiceommand', InvoiceCommandViewSet)
# #---------------------------------
# router.register(r'payment', PaymentViewSet)
# router.register(r'paymentinvoice', PaymentInvoiceViewSet)
# #---------------------------------