# -*- coding: utf-8 -*-

from django.conf import settings

def get_flutter_layouts():
    return [
		['01', '<MyApp>'],
		['01_01', '<MaterialApp>'],
		['01_01_01', '<My[xxx]Page>' ],
		['01_01_01_01', '<_My[xxx]PageState>' ],
		['01_01_01_01', '<Scaffold>'],
		['01_01_01_01_01', '<AppBar>'],
		['01_01_01_01_02', '<Center>'],
		['01_01_01_01_03', '<Foot>'],
		#--------------------------------
		['01_01_02', '<MyDashboardPage>' ]
		['01_01_03', '<MyListViewPage>' ]
		['01_01_04', '<MyCreateViewPage>' ]
		['01_01_04', '<MyUpdateViewPage>' ]
	]

def get_flutter_components():
    lista = [
		['<MyApp>', {}, ['<MaterialApp>',]],
		#----------
		['<MaterialApp>', {
			'title':'', 
			'theme':'<ThemeData>',
			'home': '<MyHomePage>',
			}, [],
		],
		#--------------
		['<ThemeData>', {
			'primarySwatch': 'Color.blue',
			}, [],
		],
		#--------------
		['<MyHomePage>', {
			'title': '', 
			'_MyHomePageState': '<_MyHomePageState>',
			}, [],
		],
		#------------------------------
		['<_MyHomePageState>', {}, ['<Scaffold>']],
		#------------------
		['<Scaffold>', {
			'appBar': '<AppBar>', 
			'body': '<Center>', 
			'floatingActionBotton':'<FloatingActionButton>'
			}, [],
		],
		#------------------
		['<AppBar>', {
			'title': '',
			}, []],
		#-----------------------
		['<Center>', {
			'title': '',
			}, [],
		],
		

	]
    return lista
