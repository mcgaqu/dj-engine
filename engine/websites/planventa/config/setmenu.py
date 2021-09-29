# -*- coding: utf-8 -*-

def get_menu_MASTER():
    from ..settings import PREFIX_URL
    from django.conf import settings
    # PREFIX_URL = ''
    return [

        [
            ['#', 'Projectos'],
            [
                ['%scompanies/company/%s/' % (PREFIX_URL, settings.SITE_ID), 'Company'],
               # ['%sdoctypes/doctype/' % PREFIX_URL, 'DocTypes'],
                ['%sprojects/project/' % PREFIX_URL, 'Project'],
                # ['%sprojects/projectaux/' % PREFIX_URL, 'ProjectAux'],
                ['%splans/plan/' % PREFIX_URL, 'Plan'],
 
            ],
        ],
        [
            ['#', 'Facturas'],
            [
                ['%splans/plancv/' % PREFIX_URL, 'Ftras Previstas'],
                ['%splans/plancvtax/' % PREFIX_URL, 'Ftras: Impuestos'],
                ['%splans/plancvproduct/' % PREFIX_URL, 'Ftras: Productos'],
                ['%spersons/person/' % PREFIX_URL, 'Personas'],
                ['%sproducts/product/' % PREFIX_URL, 'Productos'],
            ],
        ],
 
    ]

def get_menu_MANAGER():
    return get_menu_MASTER()   


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
                        'adjango', 'companies', 'doctypes', 'annexes',

                    ]
                }
            ],
        '%s_MANAGER' % site_name: [index_url_manager, get_menu_MASTER(),  {
                    'content_type__app_label__in': [
                        # 'auth',
                        'adjango', 'companies', 'doctypes', 'annexes',

                    ]
                }
            ],
    }

