# -*- coding: utf-8 -*-

# from django.conf import settings

def get_react_components():
    
	lista = [
		['<App>', {}, ['<Admin>']],
		['<Admin>', {
			'dataProvider': '',
			'authProvider': '',
			'i18Provider': '',
			'title': '', 
			'dashboard': '',
			'catcAll': '', 
			'theme': '', 
			'layout': '',
			'customReducers': '', 
			'customSagas': '',
			'customRoutes': '',
			'loginPage': '', 
			'loginButton': '',
			'initialState': '',
			'history': '',
			}, ['<AdminContext>', '<AdminUI>']
		],
		#-------------------------
		['<AdminContext>', {}, []],
		['<AdminUI', {}, ['<Resources']],
		#------------------------
		# ['<Resources>',[], ['<Resource>']],
		['<Resource>', {
			'list': '',
			'create': '',
			'edit': '',
			'show': '',
			'name': '',
			'icon': '',
			'options': '', # label
			},
		],
		#------------------------------
		['<List>', {
			'title': '', 
			'actions': '',  
			'exporter': '',
			'bulkActionsButtons': '', 
			'filters': '', 
			'filterDefaultValues': '',
			'perPage': '',
			'sort': '',
			'filter': '',
			'pagination': '',
			'aside': '',
			'empty': '',
			}, ['<Pagination>','<Datagrid>']
		],
		#=============================
		['<Pagination>', {
			'rowsperPageOptions': '',
			}, []
		]
		#=============================
		['<Datagrid>', {
			'rowClick': '',
			}, ['<TextField>', '<ReferenceField>', '<EditButton>']
		],
		#-----------------------------------	
		['<SimpleList>', {
			'primaryText': '',
			'secundaryText': '', 
			'tertiaryText': '',
			}, [],
		],			
		#-----------------------------------
		['<Create>', {
			'title': '', 
			'actions': '', 
			'aside': '',
			'component': '',
			'record': '', # only create
			'onSucces': '', 
			'onFailure': '', 
			'transform': '',
			}, [],
		],
		#-----------------------------------
		['<Edit>', {
			'title': '', 
			'actions': '', 
			'aside': '',
			'component': '', 
			'undoable': '', # only edit
			'onSucces': '',
			'onFailure': '', 
			'transform': '',
			}, []
		],
		#-----------------------------------
		['<SimpleForm>', {		
			'initialValues': '', 
			'validate': '', 
			'submitOnEnter': '',
			'rediret': '', 
			'toolbar': '', 
			'variant': '',
			'margin': '',
			'warnWhenUnsavedChanges': '', 
			'sanitizeEmptyValues': '',
			}, [],
		],
		#-----------------------------------
		['<TabbedForm', {
			'initialValues': '', 
			'validate': '', 
			'submitOnEnter': '',
			'redirect': '',
			'tabs': '', 
			'toolbar': '',
			'variant': '', 
			'margin': '',
			'save': '', 
			'saving': '',
			'warnWhenUnsavedChanges': '', 
			'sanitizeEmptyValues': '',
			}, [],
		],
		#-----------------------------------
		['<Show>', {
			'title': '', 
			'actions': '', 
			'aside': '', 
			'component': '',
			}, [],
		]
		#-----------------------------------
	]
	return lista