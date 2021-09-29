# -*- coding: utf-8 -*-

from django.conf import settings


def get_base_layout():
	return [
		# id = header -----------
		['01', 'branding'],
		['02', 'usertools'],
		['02_01', 'welcome-msg'],
		['02_02', 'userlinks'],
		['03', 'nav-global'],
		#------------------------
		['04', 'breadcrumbs'],
		# id = main -------------
		['05', 'nav-sidebar'],
		['06', 'messages'],
		['07', 'coltype'],
		['08', 'pretitle'],
		['09', 'content-title'],
		['10', 'content-subtitle'],
		['11', 'content'],
		['12', 'object-tools'],
		['13', 'sidebar'],
		#------------------
		['14', 'footer'],
	]

def get_django_layouts():
    return [
		['00', '<MainPage>', get_base_layout()],
		['01', '<LoginPage>'],
		['02', '<LogoutPage>'],
		['03', '<IndexPage>'],
		['04', '<DashboardPage>'],
		#-----------------
		['05', '<ListPage>'],
		['06', '<AddPage>'],
		['07', '<ChangePage>'],
	]

def get_django_components():
	return [
		# id = header -----------
		['01', 'branding'],
		['02', 'usertools'],
		['02_01', 'welcome-msg'],
		['02_02', 'userlinks'],
		['03', 'nav-global'],
		#------------------------
		['04', 'breadcrumbs'],
		# id = main -------------
		['05', 'nav-sidebar'],
		['06', 'messages'],
		['07', 'coltype'],
		['08', 'pretitle'],
		['09', 'content-title'],
		['10', 'content-subtitle'],
		['11', 'content'],
		['12', 'object-tools'],
		['13', 'sidebar'],
		#------------------
		['14', 'footer'],
	]