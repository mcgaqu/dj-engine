# -*- coding: utf-8 -*-

def get_menu_MASTER():
    from ..settings import PREFIX_URL
    from django.conf import settings
    # PREFIX_URL = ''
    return [

        [
            ['#', 'Resumen'],
            [
                ['%scompanies/company/%s/' % (PREFIX_URL, settings.SITE_ID), 'Empresa'],
                ['%sprojects/project/' % PREFIX_URL, 'Projects'],
                ['%splans/plan/?level=0' % PREFIX_URL, 'Plan'],
                ['%splans/plan/' % PREFIX_URL, 'Resumen CV'],
                ['%splans/planfactor/' % PREFIX_URL, 'Factores'],
 
            ],
        ],
        [
            ['#', 'Facturas'],
            [
                ['%splans/plandoc/' % PREFIX_URL, 'Ftras Previstas'],
                ['%splans/plandoctax/' % PREFIX_URL, 'Ftras: Impuestos'],
                ['%splans/plandocproduct/' % PREFIX_URL, 'Ftras: Productos'],
                ['%spersons/person/' % PREFIX_URL, 'Personas'],
                ['%sproducts/product/' % PREFIX_URL, 'Productos'],
            ],
        ],
 
    ]

def get_menu_MANAGER():
    from ..settings import PREFIX_URL
    from django.conf import settings
    # PREFIX_URL = ''
    return [

        [
            ['#', 'Resumen'],
            [
                # ['%scompanies/company/%s/' % (PREFIX_URL, settings.SITE_ID), 'Empresa'],
                # ['%sprojects/project/' % PREFIX_URL, 'Planes'],
                ['%splans/plan/?level=0' % PREFIX_URL, 'Plan CV'],
                ['%splans/plan/' % PREFIX_URL, 'Resumen CV'],
                ['%splans/planfactor/' % PREFIX_URL, 'Factores'],
 
            ],
        ],
        [
            ['#', 'Facturas'],
            [
                ['%splans/plandoc/' % PREFIX_URL, 'Ftras Previstas'],
                ['%splans/plandoctax/' % PREFIX_URL, 'Ftras: Impuestos'],
                ['%splans/plandocproduct/' % PREFIX_URL, 'Ftras: Productos'],
                ['%spersons/person/' % PREFIX_URL, 'Personas'],
                ['%sproducts/product/' % PREFIX_URL, 'Productos'],
            ],
        ],
 
    ]

def get_menu_EMPLOYEE():
    return [

    ]

def get_menu_CUSTOMER():
    return [
 
    ]


def get_MENUS():
    # from ..settings import PREFIX_URL
    from django.conf import settings

    site_name = settings.SITE_NAME
    index_url_master = "companies/company/%s/change/" % settings.SITE_ID
    index_url_manager = "companies/company/%s/change/" % settings.SITE_ID
    return  {
        '%s_MASTER' % site_name: [index_url_master, get_menu_MASTER(),  {
                    'content_type__app_label__in': [
                        # 'auth',
                        'adjango', 'companies', 'doctypes',
                        'persons', 'products', 'projects',
                        'plans'
                    ]
                }
            ],
        '%s_MANAGER' % site_name: [index_url_manager, get_menu_MASTER(),  {
                    'content_type__app_label__in': [
                        # 'auth',
                        'adjango', 'companies', 'doctypes',
                        'persons', 'products', 'projects',
                        'plans'
                    ]
                }
            ],
    }

#=========================
def x_get_MENUS():
        index_url_master = "companies/company/?active=1"
        index_url_manager = "companies/company/?active=1&bloqueado=0"
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
