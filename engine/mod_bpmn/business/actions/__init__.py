# -*- coding: utf-8 -*-

# from .ac_biz import load_BUSINESS, load_menus, load_apps, load_models, load_layouts, load_components
# from .ac_company import load_COMPANY, load_company1, load_CompanyProp

from .actions1 import (
    load_BPMN,
    load_data, # load_BApp, load_BModel,
    load_datastate,
    load_layouts, # load_Component, load_Layout
    )

from .actions2 import (
    load_mdas, 
    )


def get_app_actions(index):
    dev = {
        'Biz': [
            load_BPMN,
            load_data,
            load_datastate,
            load_layouts,
            load_mdas,
            # load_cocklists,
            # load_tasklist
        ],
    }
    return dev[index]

