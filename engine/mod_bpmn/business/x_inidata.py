# -*- coding: utf-8 -*-
from django.conf import settings

#=============================
def get_components(grade='django'):
	if grade == 'django':
    	return get_django_components()


# def x_get_components(grade='django'):
# 	if grade == 'django':
# 		return get_django_components()
# 	elif grade == 'flutter':
#     	return get_flutter_components()
# 	elif grade == 'react':
# 		return get_react_components()
# 	# elif grade == 'vue':
# 	# 	return get_vue_component()
# 	else:
#     	return

def get_django_components():
	return [
		# todas las vistas estandard en el ModelAdmi1
		# las de django admin + piezas del modelo de negocio
		#----------------
		['<Admin>', [
			'title', 'dashboard', 
			'layout', #base_site.html'
		]],
		#--------------------
		['<index>', [
			'template', # index.html
		]],
		['<login>', []],
		['<logout>', []],
		['<jsi18n>', []],
		#-------------------
		['<Resource>', [
			'list', 'create', 'edit', 'show',
			'name', 'icon', 'options' # label
		]],
		#-----------------------
		['<changelist>', [
			'list_display', 'list_filter',
			'actions'
		]],
		['<add>', [
			'fieldsets', 'inlines', 
		]],
		['<change>', [
			'fieldsets', 'inlines', 'object_tools'
		]],
		['<autocomplete>',[]],
		['<history>', []],
		['<delete>', []],
		# pieza <Pieza???>
		['<password>', []],
		#-------------------------
		['<inlines>', [
			'fields', 'extra', 
		]],

	]

def get_flutter_components():
    lista = [
		# ['<App>', [], ['<Admin>']],
		['<Admin>', [
			'dataProvider', 'authProvider', 'i18Provider',
			'title', 'dashboard', 'catcAll', 
			'theme', 'layout',
			'customReducers', 'customSagas', 'customRoutes',
			'loginPage', 'loginButton', 'initialState',
			'history' 
			], ['<AdminContext>', '<AdminUI>']],
	]
	return lista

def get_react_components():

	lista = [
		# ['<App>', [], ['<Admin>']],
		['<Admin>', [
			'dataProvider', 'authProvider', 'i18Provider',
			'title', 'dashboard', 'catcAll', 
			'theme', 'layout',
			'customReducers', 'customSagas', 'customRoutes',
			'loginPage', 'loginButton', 'initialState',
			'history' 
			], ['<AdminContext>', '<AdminUI>']],
		['<AdminContext>', [], []],
		['<AdminUI', [], ['<Resources']],
		#------------------------
		# ['<Resources>',[], ['<Resource>']],
		['<Resource>', [
			'list', 'create', 'edit', 'show',
			'name', 'icon', 'options' # label
		]],
		#------------------------------
		['<List>', [
			'title', 'actions',  'exporter',
			'bulkActionsButtons', 
			'filters', 'filterDefaultValues',
			'perPage', 'sort', 'filter',
			'pagination', 'aside', 'empty'
			], ['<Pagination>','Datagrid' ]],
		#=============================
		['<Pagination>', [
			'rowsperPageOptions'
			], []],
		['<Datagrid>', [
			'rowClick'
			], ['<TextField>', '<ReferenceField>', '<EditButton>']],	
		['<SimpleList>', [
			'primaryText', 'secundaryText', 'tertiaryText'
			], []],			
		#-----------------------------------
		['<Create>', [
			'title', 'actions', 'aside',
			'component', 'record' # only create
			'onSucces', 'onFailure', 'transform'
		]],
		['<Edit>', [
			'title', 'actions', 'aside',
			'component', 'undoable', # only edit
			'onSucces', 'onFailure', 'transform'
		]],
		['<SimpleForm>', [
			'initialValues', 'validate', 'submitOnEnter',
			'rediret', 'toolbar', 'variant', 'margin',
			'warnWhenUnsavedChanges', 'sanitizeEmptyValues'
		]],
		['<TabbedForm',[
			'initialValues', 'validate', 'submitOnEnter',
			'redirect', 'tabs', 'toolbar', 'variant', 'margin',
			'save', 'saving',
			'warnWhenUnsavedChanges', 'sanitizeEmptyValues'
		]],
		['<Show>', [
			'title', 'actions', 'aside', 'component'
		]]
	]
	return lista

def get_Layout():
	lista = [
		# ['0','admin'],
		# ['000', 	'property'],
		# ['000x', 		'title',],
		['01',	'layout',],
		['011',		'appbar'],
		['0111',		'usermenu'],
		['012', 	'aside'],
		['0121',		'menu'],
		['013',		'content'],
		['0131',		'dashboard'],
		['0132',		'mod'],
		['01321',			'app'],
		['013211', 				'actions'],
		['013212', 				'resource'],
		['0132121', 				'model'],
		['0132122', 				'modeladmin'],
		['01321221', 					'viewList'],
		['013212211', 						'toolList'],
		['0132122111', 							'arcoList'],
		['01321222', 					'viewCreate'],
		['013212221', 						'toolCreate'],
		['01321223', 					'viewUpdate'],
		['013212231', 						'toolUpdate'],
		['0132122311', 							'arcoUpdate'],
		['013213', 				'apirest'],
		['013214', 				'apigql'],
		['013215', 				'appdashboard'],
		['01322',			'moddashboard'],

	] 
	return lista

#=============================

def get_MdaX():
	return {
	}

def get_viewcs():
	return [ # tipo, vista, param_template, template_html
		['site', 'login', 'login_template', 'admin/login.html'],
		['site', 'logout', 'logout_template', 'admin/logout.html'],
		['site', 'index', 'index_template', 'admin/index.html'],
		['site', 'appindex', 'appindex_template', 'admin/appindex.html'],
		['model', 'change_view', 'add_form_template', 'admin/change_form.html'],
		['model', 'add_view', 'change_form_template', 'admin/change_form.html'],
		['model', 'changelist_view', 'change_list_template', 'admin/change_list.html'],
		['model', 'delete_view', 'popup_response_template', 'admin/popup_response.html'],
		['model', 'history_view', 'object_history_template', 'admin/object_history.html'],
		[]
	]

	
def x_get_Component():
	return [
		'title', 
		'stylesheet', 'stylesheet_rtl',
		'extrastyle', 'extrahead', 'responsive'
		'blockbots',
		'bodyclass',
		#----------------header
		'branding',
		'usertools',
			'welcome-msg',
			'userlinks',
		'nav-global',
		#------------------
		'breadcrumbs',
		#----------------main
			'nav-sidebar',
			#----------content
			'messages',
			#----------content
			'coltype',
			'pretitle',
			'content-title',
			'content',
			'object-tools', 'object-tools-items',
			'sidebar',
		#--------------footer
		'footer',
		#---------------change_list.html
		'search',
		'date-fierarchy',
		'filters',

	]





def get_ViewcX():
	return [
		['index',[
			['index_template', {'valuex': 'admin/index.html'}],
			['index_title',{'valuex': "Indice"}],
			],
		],
		['change',[
			['change_template', {'valuex': 'admin/index.html'}],
			['change_title',{'valuex': "Modificacion"}],
			]
		],

	]

def x_get_BizX():
	res = {}
	for clave, datos in get_sitioparams_S().items():
		res[(clave, 'S')] = datos
	for clave, datos in get_sitioparams_A().items():
		res[(clave, 'A')] = datos
	for clave, datos in get_sitioparams_I().items():
		res[(clave, 'I')] = datos
	return res


def get_sitioparams_S():
	dev = {
	'site_title':  {'grade':'base', 'tags':'base', 'sort':'01', 'internal':1},
	'site_header': {'grade':'base', 'tags':'base', 'sort':'02', 'internal':1},
	'index_title': {'grade':'index', 'tags':'base', 'sort':'03', 'internal':1},
	'site_url':    {'grade':'base', 'tags':'base', 'sort':'04', 'internal':1},

	#---------------------------------
	'_empty_value_display': {'grade':'base','tags':'base', 'sort':'31', 'internal':1, 'active':0},
	'login_form': {'grade':'login', 'tags':'base', 'sort':'32', 'internal':1, 'active':0},
	#----------------------------
	'index_template': {'grade':'index', 'tags':'template', 'sort':'11', 'internal':1},
	'app_index_template': {'grade': 'index', 'tags': 'template', 'sort':'12', 'internal':1},
	'login_template': {'grade': 'login', 'tags': 'template', 'sort':'13', 'internal':1},
	'logout_template': {'grade': 'login', 'tags': 'template', 'sort':'14', 'internal':1},
	'password_change_template': {'grade': 'login', 'tags': 'template', 'sort':'15', 'internal':1},
	'password_change_done_template': {'grade': 'login', 'tags': 'template', 'sort':'16', 'internal':1},
	#-----------------------
	# userlinks
	#------------------------
	'logo_site':   {'grade':'base', 'tags':'base', 'internal':0, 'sort':'19',
					'active':0, 'name': "Logo Sitio", 'valuex':'', },
	'wellcome': {'grade': 'base', 'tags': 'userlinks', 'internal':1, 'sort':'20',
			   'active':0, 'name': 'Bienvenido', 'valuex': ''},
	'verSitio': {'grade': 'base', 'tags': 'userlinks', 'internal':1, 'sort':'21',
			   'active':0, 'name': 'Ver Sitio', 'valuex': ''},
	'idioma': {'grade': 'base', 'tags': 'userlinks', 'internal':0, 'sort':'22',
			   'active':0, 'name': 'Idioma', 'valuex': 'es-es'},

	'theme': {'grade': 'base', 'tags': 'userlinks', 'internal':0, 'sort': '23',
			  'active':0, 'name': 'Estilo', 'valuex': 'base_azul'},
	
	'avisos': {'grade': 'base', 'tags': 'userlinks', 'internal':0, 'sort': '24',
			   'active':0, 'name': "Avisos", 'valuex':'/admin1miaviso/'},
	
	'ayuda': {'grade': 'base', 'tags': 'userlinks', 'internal':0, 'sort': '25',
			   'active':0, 'name': "Ayuda", 'valuex':'/docmenu/0/'},

	'miCuenta': {'grade': 'base', 'tags': 'userlinks', 'internal':0, 'sort': '26',
			   'active':0, 'name': "Ayuda", 'valuex':'https://www.irisapp.net/admin1micuenta/'},

	'soporte': {'grade': 'base', 'tags': 'userlinks', 'internal':0, 'sort': '27',
			   'active':0, 'name': "Soporte", 'valuex':'https://www.irisapp.net/sicemsl/admin1soporte/'},

	'cambiaClave': {'grade': 'base', 'tags': 'userlinks', 'internal':1, 'sort': '28',
			   'active':0, 'name': "Cambia Clave",'valuex':'/password_change/'},
	
	'logout': {'grade': 'base', 'tags': 'userlinks', 'internal':1, 'sort': '29',
				'active':0, 'name': "Terminar Sesión", 'valuex':'/logout/', },

	}
	return dev


def get_sitioparams_AI():
	return {
		'verbose_name': {'grade': 'form', 'tags': 'base', 'internal':1, 'sort':'103',
			'name': 'Título', 'valuex':'', 'active':1},

		'verbose_name_plural': {'grade': 'list', 'tags': 'base', 'internal':1, 'sort':'104',
			'name': 'Título plural', 'valuex':'', 'active':1},

		'ordering': {'grade':'list', 'tags':'base', 'internal':1, 'sort':'110',
					'name':'', 'valuex':[], 'active':1},
		'filtro_queryset': {'grade':'list', 'tags':'base', 'internal':0, 'sort':'120',
					'name':'', 'valuex':{}, 'active':1},
		'sufijo_inicial': {'grade':'list', 'tags':'base', 'internal':0, 'sort':'130',
					'name':'', 'valuex':"", 'active':1},

		#---------------------------------

		'add_fieldsets': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'510',
					'name':'', 'valuex':[], 'active':1},
		'fieldsets': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'511',
					'name':'', 'valuex':[], 'active':1},
		'fieldsets_popup': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'512',
					'name':'', 'valuex':[], 'active':1},
		'fields': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'520',
					'name':'', 'valuex':[], 'active':1},
		
		'exclude': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'521',
					'name':'', 'valuex':[], 'active':1},



		'readonly_fields': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'541',
					'name':'', 'valuex':[], 'active':1},

		'autocomplete_fields': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'542',
					'name':'', 'valuex':[], 'active':1},
		
		'raw_id_fields': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'543',
					'name':'', 'valuex':[], 'active':1},

		
		'filter_horizontal': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'544',
					'name':'', 'valuex':[], 'active':0},
		
		'filter_vertical': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'545',
					'name':'', 'valuex':[], 'active':0},
		
		'radio_fields': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'546',
					'name':'', 'valuex':[], 'active':0},
		
		'prepopulated_fields': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'547',
					'name':'', 'valuex':[], 'active':0},

		'campos_obligatorios': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'548',
					'name':'', 'valuex':[], 'active':1},

		#--------------------------
		'form_etiquetas': {'grade':'form', 'tags':'campos', 'internal':1, 'sort':'610',
					'name':'', 'valuex':[], 'active':1},
		'list_etiquetas': {'grade':'list', 'tags': 'campos', 'internal':0, 'sort':'611',
				'name':'', 'valuex':'', 'active':1},
		'widgets_attrs': {'grade':'form', 'tags':'campos', 'internal':1, 'sort':'630',
					'name':'', 'valuex':[], 'active':1},

		'definidos': {'grade':'form', 'tags':'campos', 'internal':1, 'sort':'640',
					'name':'', 'valuex':[], 'active':1},
		'filtro_fk_fields': {'grade':'form', 'tags':'campos', 'internal':1, 'sort':'650',
					'name':'', 'valuex':[], 'active':1},

		'initial_data': {'grade':'form', 'tags':'campos', 'internal':1, 'sort':'660',
					'name':'', 'valuex':[], 'active':1},
		'campos_del_padre': {'grade':'form', 'tags':'field_sets', 'internal':0, 'sort':'671',
					'name':'', 'valuex':'', 'active':0},
		'campos_del_tronco': {'grade':'form', 'tags':'field_sets', 'internal':0, 'sort':'672',
					'name':'', 'valuex':'', 'active':0},


		#--------------------------------------------		

		'grade_on_site': {'grade':'form', 'tags':'field_sets', 'internal':1, 'sort':'800',
					'name':'', 'valuex':[], 'active':0},

	}


def get_sitioparams_A():
	dev = get_sitioparams_AI()
	dev.update({
		#--------------------------------------
		# CHANGE LIST: 
		#----------------------------------
		
		#  1xx vienen de  get_sitioparams_AI()

		'titulo_list': {'grade':'list', 'tags':'base', 'internal':0, 'sort':'200',
					'name':'', 'valuex':'', 'active':1},


		'list_display': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'201',
					'name':'', 'valuex':[], 'active':1},
		'list_display_links': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'202',
					'name':'', 'valuex':[], 'active':1},
		'list_editable': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'203',
					'name':'', 'valuex':[], 'active':1},

		'date_hierarchy': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'204',
					'name':'', 'valuex':100, 'active':1},
		'list_filter': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'205',
					'name':'', 'valuex':[], 'active':1},

		'list_filterx': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'206',
					'name':'', 'valuex':[], 'active':0},



		'search_fields': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'210',
					'name':'', 'valuex':[], 'active':1},
		
	
		'list_select_related': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'214',
					'name':'', 'valuex':0, 'active':0},
		'list_per_page': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'215',
					'name':'', 'valuex':100, 'active':0},
		'list_max_show_all': {'grade':'list', 'tags':'result_list', 'internal':1, 'sort':'216',
					'name':'', 'valuex':200, 'active':0},
		'paginator': {'grade':'list', 'tags':'list', 'internal':1, 'sort':'217',
					'name':'', 'valuex':'Paginator', 'active':0},
		'show_full_result_count': {'grade':'list', 'tags':'list', 'internal':1, 'sort':'218',
					'name':'', 'valuex':[], 'active':0},
		'preserve_filters': {'grade':'list', 'tags':'list', 'internal':1, 'sort':'220',
					'name':'', 'valuex':1, 'active':0},

		#--------------------------------------
	
		# 'actions': {'grade':'list', 'tags':'actions', 'internal':1, 'sort':'310',
		# 			'name':'','valuex':[], 'active':1},
		# 'tool_list': {'grade':'list', 'tags': 'object-tools', 'internal':0, 'sort':'320',
		# 			'name':'', 'valuex':'', 'active':1},

		#--------------------------------------
		# CHANGE FORM: 
		#----------------------------------

		'titulo_form': {'grade':'form', 'tags':'base', 'internal':0, 'sort':'400',
					'name':'', 'valuex':'', 'active':1},

		#---- 500 y 600 vienene de  get_sitioparams_AI()

		'save_as': {'grade':'form', 'tags':'submit', 'internal':1, 'sort':'710',
					'name':'', 'valuex':0, 'active':0},
		'save_as_continue': {'grade':'form', 'tags':'submit', 'internal':1, 'sort':'711',
					'name':'', 'valuex':1, 'active':0},
		'save_on_top': {'grade':'form', 'tags':'submit', 'internal':1, 'sort':'712',
					'name':'', 'valuex':0, 'active':0},

		# 'add_inlines': {'grade':'form', 'tags':'inline_field_sets', 'internal':0, 'sort':'721',
		# 			'name':'', 'valuex':[], 'active':1},
		# 'inlines': {'grade':'form', 'tags':'inlines', 'internal':1, 'sort':'722',
		# 			'name':'', 'valuex':[], 'active':1},

		# 'tool_form': {'grade':'form', 'tags': 'object-tools', 'internal':0, 'sort':'810',
		# 			'name':'', 'valuex':'', 'active':1},
		# 'tool_before_change': {'grade':'form', 'tags': 'before-change', 'internal':0, 'sort':'811',
		# 			'name':'', 'valuex':'', 'active':0},
		# 'tool_before_delete': {'grade':'form', 'tags': 'before-delete', 'internal':0, 'sort':'812',
		# 			'name':'', 'valuex':'', 'active':0},
		# 'tool_after_add': {'grade':'form', 'tags': 'after-add', 'internal':0, 'sort':'813',
		# 			'name':'', 'valuex':'', 'active':0},
		# 'tool_after_change': {'grade':'form', 'tags': 'after-change', 'internal':0, 'sort':'814',
		# 			'name':'', 'valuex':'', 'active':0},
		# 'tool_after_delete': {'grade':'form', 'tags': 'after-delete', 'internal':0, 'sort':'815',
		# 			'name':'', 'valuex':'', 'active':0},

		#-----------------------------------
		# INFORMES
		# #---------------------------------
		'campos_informes': {'grade':'info', 'tags':'field_sets', 'internal':0, 'sort':'549',
					'name':'', 'valuex':[], 'active':0},


		#============================================
		# ADMIN plantillas
		#------------------------------
		'add_form_template': {
		    'grade': 'add', 'tags': 'templates', 'internal':1, 'sort':'901',
		    'name':'', 'valuex': 'admin/change_form.html', 'active':0},
		'change_form_template': {
			'grade': 'form', 'tags': 'templates',  'internal':1, 'sort':'902',
			'name':'','valuex': 'admin/change_form.html','active':0},
		'change_list_template': {
			'grade': 'list', 'tags': 'templates', 'internal':1, 'sort':'903',
			'name':'', 'valuex': 'admin/change_list.html','active':0},
		'delete_confirmation_template': {
			'grade': 'delete', 'tags': 'templates', 'internal':1, 'sort':'904',
			'name':'', 'valuex': 'admin/delete_confirmation.html', 'active':0},
		'delete_selected_confirmation_template': {
			'grade': 'list', 'tags': 'templates', 'internal':1, 'sort':'905',
			'name':'', 'valuex': 'admin/delete_selected_confirmation.html', 'active':0},
		'object_history_template': {
			'grade': 'history', 'tags': 'templates', 'internal':1, 'sort':'906',
			'name':'', 'valuex': 'admin/object_history.html', 'active':0},
		'popup_response_template': {
			'grade': 'base', 'tags': 'templates', 'internal':1, 'sort':'907',
			'name':'', 'valuex': 'admin/popup_response.html',  'active':0},
		#--------------------
		'listform_template': {
			'grade': 'form', 'tags': 'templates', 'internal':0, 'sort':'908',
			'name':'', 'valuex': 'listform.html','active':0},
		'agenda_template': {
			'grade': 'list', 'tags': 'templates', 'internal':0, 'sort':'909',
			'tipo_dato': '.html', 'valuex': 'agenda.html','active':0},
		'ayuda_template': {
			'grade': 'list', 'tags': 'templates', 'internal':0, 'sort':'910',
			'name':'', 'valuex': 'agenda.html', 'active':0},
		#==============================================

	})		
	return dev

def get_sitioparams_I():
	dev = get_sitioparams_AI()
	dev.update({
		#============================================
		# Inline plantillas
		#------------------------------


		'classes': {'grade':'inline', 'tags':'inlines', 'internal':1, 'sort':'303',
					'name':'', 'valuex':'InlineModelAdminChecks', 'active':0},

		'extra': {'grade': 'form', 'tags': 'inlines', 'internal':1,  'sort':'313',
			'name':'', 'valuex':0, 'active':1},
		'min_num': {'grade': 'form', 'tags': 'inlines', 'internal':1,  'sort':'314',
			'name':'', 'valuex':None, 'active':1},
		'max_num': {'grade': 'form', 'tags': 'inlines', 'internal':1,  'sort':'315',
			'name':'', 'valuex':None, 'active':1},


		'can_delete': {'grade':'form', 'tags':'inlines', 'internal':1, 'sort':'617',
					'name':'', 'valuex':1, 'active':1},


		#------------------------------
		'carga_datox': {'grade':'form', 'tags':'inlines', 'internal':0, 'sort':'701',
					'name':'', 'valuex':0, 'active':0},

		'datox_regs': {'grade':'form', 'tags':'inlines', 'internal':0, 'sort':'702',
					'name':'', 'valuex':[], 'active':0},

		'campox_fields': {'grade':'form', 'tags':'inlines', 'internal':0, 'sort':'703',
					'name':'', 'valuex':[], 'active':0},
		'datox_fields': {'grade':'form', 'tags':'inlines', 'internal':0, 'sort':'704',
					'name':'', 'valuex':[], 'active':0},
		#-------------------------------
		'tool_inline': {'grade':'form', 'tags': 'inlines', 'internal':0, 'sort':'710',
					'name':'', 'valuex':'', 'active':0},
		#-------------------------------------
		'show_change_link': {'grade':'form', 'tags':'inlines', 'internal':1, 'sort':'801',
					'name':'', 'valuex':1, 'active':1},

		'inline_template': {'grade': 'form', 'tags': 'inlines', 'internal':1, 'sort':'950',
			'name': '', 'valuex': 'admin/edit_inline/tabular.html', 'active':0},
	})		
	return dev
