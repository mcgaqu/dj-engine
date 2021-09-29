# -*- coding: utf-8 -*-

from rest_framework import routers
from rest_framework.pagination import PageNumberPagination

from mod_auth.adjango.apirest import UserViewSet, GroupViewSet
from mod_auth.companies.apirest import CompanyViewSet, CompanyPropViewSet, MenuViewSet, MenuItemViewSet
from mod_auth.doctypes.apirest import DocTypeViewSet, DocTypePropViewSet
# from mod_bpmn.companies.apirest import BizViewSet
# from mod_bpmn.data.apirest import BAppViewSet, BModelViewSet, BModelFieldViewSet. BModelActionViewSet
# from mod_bpmn.datastate.apirest import ComponentViewSet, CompPropViewSet
# from mod_bpmn.layouts.apirest import CmsViewSet, ComponentViewSet, ElementViewSet
# from mod_bpmn.mdas.apirest import WebSetViewSet, WebSetElementViewSet

from mod_entity.persons.apirest import SegmentViewSet, CustomerViewSet
from mod_entity.products.apirest import CategoryViewSet, ProductViewSet, ProductAuxViewSet 
from mod_entity.projects.apirest import ProjectViewSet, ExpedientViewSet, ExpedientAuxViewSet
from mod_make.tasks.apirest import TaskViewSet, TaskAuxViewSet
from mod_make.works.apirest import WorkViewSet, WorkAuxViewSet

from mod_order.commands.apirest import CommandViewSet,  CommandAuxViewSet
from mod_order.invoices.apirest import InvoiceViewSet,  InvoiceAuxViewSet
# from mod_order.payments.apirest import PaymentViewSet,  PaymentInvoiceViewSet

#===========================================

class PageNumberPagination1(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 10000


router = routers.DefaultRouter()
#--------------------------------
router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
#-------------------

router.register(r'company', CompanyViewSet)
router.register(r'companyprop', CompanyPropViewSet)

router.register(r'menu', MenuViewSet)
router.register(r'menuitem', MenuItemViewSet)
router.register(r'doctype', DocTypeViewSet)
router.register(r'doctypeprop', DocTypePropViewSet)
#-------------------

router.register(r'segment', SegmentViewSet)
router.register(r'customer', CustomerViewSet)
#-------------------
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'productaux', ProductAuxViewSet)
#---------------------------------
router.register(r'project', ProjectViewSet)
router.register(r'expedient', ExpedientViewSet)
router.register(r'expedientaux', ExpedientAuxViewSet)
#---------------------------------
router.register(r'task', TaskViewSet)
router.register(r'taskaux', TaskAuxViewSet)
router.register(r'work', WorkViewSet)
router.register(r'workaux', WorkAuxViewSet)
#---------------------------------
router.register(r'command', CommandViewSet)
router.register(r'commandaux', CommandAuxViewSet)
# router.register(r'commandproduct', CommandAuxViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'invoiceaux', InvoiceAuxViewSet)
# router.register(r'invoiceproduct', CommandAuxViewSet)

# router.register(r'payment', PaymentViewSet)
# router.register(r'paymentinvoice', PaymentInvoiceViewSet)
#=====================================

