# -*- coding: utf-8 -*-

def get_menu_MASTER():
    return [
        [
            ['#', 'Aplicación'],
            [
                ['business/biz/', 'Aplicación'],
                ['business/company/', 'Empresas'],
                ['auth/permission/', 'Permisos'],
                ['sessions/session/', 'Sesiones'],
                ['admin/logentry/', 'Entradas de Registro'],
                # ['auth/group/', 'Grupos'],
                # ['auth/user/', 'Usuarios'],
                # ['business/menus/', 'Menus'],
                # ['company/typedoc/', 'Tipos de Documento']
            ],
        ],
        [
            ['#', 'BPMN'],
            [
                ['data/bapp/', 'Módulos'],
                ['data/bmodel/', 'Modelos de Datos'],
                ['datastate/baction/', '** Actions'],
                ['datastate/breducer/', '** Reducers'],
                ['datastate/bstore/', '** Store'],
                ['layout/component/', 'Componentes'],
                ['layout/layout/', 'Plantillas/Pagina'],
                ['mdas/mda/', 'Procesos'],
            ],
        ],
    ]

def get_menu_MANAGER():
    return [
        [
            ['#', 'Empresa'],
            [
                ['business/company/', 'Empresas'],
                ['auth/group/', 'Grupos'],
                ['auth/user/', 'Usuarios'],
                ['business/menus/', 'Menus'],
                ['company/typedoc/', 'Tipos de Documento'],
            ],
        ],
    ]

def get_menu_EMPLOYEE():
    return [
        [
            ['#', 'Maestros'],
            [
                ['business/company/', 'Empresas'],
                ['auth/group/', 'Grupos'],
                ['auth/user/', 'Usuarios'],
                ['business/menus/', 'Menus'],
                ['company/typedoc/', 'Tipos de Documento'],
            ],
        ],
        [
            ['#', 'Entidades'],
            [
                ['entity/persons/', 'Personas'],
                ['entity/products/', 'Productos'],
            ],
        ],
        [
            ['#', 'Neod'],
            [
                ['neod1/empresas/', 'Empresas'],
                ['neod1/tecnicos/', 'Técnicos'],
            ],
        ],
    ]

def get_menu_CLIENTE():
    return [
        [
            ['#', 'Maestros'],
            [
                ['business/company/', 'Empresas'],
                ['auth/group/', 'Grupos'],
                ['auth/user/', 'Usuarios'],
                ['business/menus/', 'Menus'],
                ['company/typedoc/', 'Tipos de Documento'],
            ],
        ],
        [
            ['#', 'Entidades'],
            [
                ['entity/persons/', 'Personas'],
                ['entity/products/', 'Productos'],
            ],
        ],
        [
            ['#', 'Neod'],
            [
                ['neod1/clientes/', 'Cliente'],
                ['neod1/cab_ventas/', 'Ventas'],
            ],
        ],
    ]

def get_menu_PROVEEDOR():
    return [
        []
    ]

def get_MENUS():
        index_url_master = "business/biz/?active=1"
        index_url_manager = "company/?active=1&bloqueado=0"
        index_url_employee = "proyex/expdte/?active=1&bloqueado=0"
        index_url_cliente = "proyex/expdte/?active=1"
        index_url_proveedor = "proyex/expdte/?active=1"
        index_url_wp = "" # "%swp/" % prefix_url

        return {
            'MASTER': 	[index_url_master, get_menu_MASTER(),  {
                            'content_type__app_label__in': [
                            #'auth',
                            'adjango', 'business', 'companies',
                            'data', 'datastate', 'layouts', 'mdas',
                            'typedocs', 'annexes', # 'jobcrons',
                            'persons', 'products', 'projects',
                            'neod1', 'neod2', 'neod3',

                             ]}
                        ],

            'MANAGER':  [index_url_manager, get_menu_MANAGER(), {
                            'content_type__model__in': [
                                'group', 'user',
                                'company', 'companyaux',
                                'rol', 'rolmenu',
                                'typedoc', 'typedocaux'
                                'neod1', 'neod2', 'neod3',
                    
                            ]}
                        ],
                        
            'EMPLOYEE':  [index_url_employee, get_menu_EMPLOYEE(), {
                            'content_type__app_label__in': [
                                'annexes',
                                'persons', 'products', 'projects',
                                'neod1', 'neod2', 'neod3',
                             ]}
                        ],

            'CLIENTE': [index_url_cliente, get_menu_CLIENTE(), {
                    'content_type__app_label__in': [
                                'annexes',
                                'persons', 'products', 'projects',
                                'neod1', 'neod2', 'neod3',
                             ]} 
            			],

            'PROVEEDOR': [index_url_proveedor, [], { 
                    'content_type__app_label__in': [
                                'annexes',
                                'persons', 'products', 'projects',
                                'neod1', 'neod2', 'neod3',
                             ]} 
            			],

            'WEBPUBLICA': [index_url_wp, [], {
            				'codename__in':['add_user']}],
        }
