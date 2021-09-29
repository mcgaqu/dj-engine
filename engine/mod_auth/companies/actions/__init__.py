# -*- coding: utf-8 -*-


from .actions1 import (
    ac_load_CompanyLoad,
    load_Company,
    load_CompanyProp, 
    load_rols,
    load_general_menu,
    load_rol_menus,
    #-----------
    load_DocType, 
    load_Project,   
    )

from .actions2 import (
    ac_import_data,
)

def get_app_actions(index):
    dev = {
        'Company': [
            ac_load_CompanyLoad,
            # copias_seguridad        
        ],
        'CompanyLoad' : [
            ac_import_data,
            #------------
        ]
    }
    return dev[index]

def get_app_functions(index):
    dev = {
        'Company': [
            ac_load_CompanyLoad,
            #-------
            load_Company,
            load_CompanyProp,
            load_rols,
            load_general_menu,
            load_rol_menus,
            #----
            load_DocType,
            load_Project,    
            # copias_seguridad        
        ],
        'CompanyLoad' : [
            ac_import_data,
            #------------
        ]
    }
    return dev[index]

