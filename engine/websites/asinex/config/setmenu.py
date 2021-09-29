# -*- coding: utf-8 -*-

def get_menu_MASTER():
    from ..settings import PREFIX_URL
    from django.conf import settings
    # PREFIX_URL = ''
    return [

        [
            ['#', 'Contenido'],
            [
                ['%scompanies/company/%s/' % (PREFIX_URL, settings.SITE_ID), 'Company'],
                ['%sdoctypes/doctype/' % PREFIX_URL, 'DocTypes'],
                ['%sannexes/folder/?level=0' % PREFIX_URL, 'Folder']
 
            ],
        ],
        # [
        #     ['#', 'Facturas'],
        #     [
        #         ['%splans/plandoc/' % PREFIX_URL, 'Ftras Previstas'],
        #         ['%splans/plandoctax/' % PREFIX_URL, 'Ftras: Impuestos'],
        #         ['%splans/plandocproduct/' % PREFIX_URL, 'Ftras: Productos'],
        #         ['%spersons/person/' % PREFIX_URL, 'Personas'],
        #         ['%sproducts/product/' % PREFIX_URL, 'Productos'],
        #     ],
        # ],
 
    ]

def get_menu_MANAGER():
    from ..settings import PREFIX_URL
    from django.conf import settings
    # PREFIX_URL = ''
    return []
    # return [

    #     [
    #         ['%sannexes/folder/?level=0' % PREFIX_URL, 'Contenido'],
    #         [
    #         ],
    #     ],
    # ]


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
    index_url_manager = "annexes/folder/"
    return  {
        '%s_MASTER' % site_name: [index_url_master, get_menu_MASTER(),  {
                    'content_type__app_label__in': [
                        # 'auth',
                        'adjango', 'companies', 'doctypes', 'annexes',

                    ]
                }
            ],
        '%s_MANAGER' % site_name: [index_url_manager, get_menu_MANAGER(),  {
                    'content_type__app_label__in': [
                        # 'auth',
                        'adjango', 'companies', 'doctypes', 'annexes',

                    ]
                }
            ],
    }

