
#-----------
# Company
#--------------

DATA_LOAD = [
 
    ['mod_auth.companies.actions', 'load_Company', 'Cargar Company', {}],
    ['mod_auth.companies.actions', 'load_CompanyProp', 'Cargar Company Props', {}],
    ['mod_auth.companies.actions', 'load_rols', 'Cargar Rols', {}],
    ['mod_auth.companies.actions', 'load_general_menu', 'Cargar General Menu', {}],
    ['mod_auth.companies.actions', 'load_rol_menus', 'Cargar Rol Menus', {}],
    #-----------------------
    ['engine.config.dataload', 'load_Folder', 'Cargar Folders: DocType + Folder', {},],
    # ['websites.asinex.config.dataload', 'load_Folder', 'Cargar Folders: DocType + Folder', {},],    

]


#========================
DATA_COMPANY = {
    'name': 'Software Integrado para el control de EMpresa',
    'tin':'B18521971', 
    'state': "España"
}



#---------------------
DATA_COMPANYPROP = [

]

DATA_FOLDER = [
    ['es', 'español',
        ['Idioma', 'contacto', 'home', 'Asesoría Legal',
            'Servicios Fiscales y Contables', 'ECCO', 
            'Inmobiliaria', 'Otros Servicios', 
            'Información de Interés','El Equipo',
        ],
    ],
    ['en', 'english',
        ['Language', 'contact', 'home', 'Legal Consultancy',
            'Accounting and TaxServices', 'ECCO', 
            'Real State', 'Other Services', 
            'Information of Interest' , 'The Team',
        ],
    ],
    ['de', 'deutsh',
        ['Idioma', 'contacto', 'home', 'Asesoría Legal',
            'Servicios Fiscales y Contables', 'ECCO', 
            'Inmobiliaria', 'Otros Servicios', 
            'Información de Interés', 'El Equipo',
        ],
    ],
    ['fr', 'francais',
        ['Idioma', 'contacto', 'home', 'Asesoría Legal',
            'Servicios Fiscales y Contables', 'ECCO', 
            'Inmobiliaria', 'Otros Servicios', 
            'Información de Interés', 'El Equipo',
        ],    
    ],
]



def load_Folder(modeladmin, request, obj):
    from django.conf import settings
    from importlib import import_module
    from mod_auth.doctypes.models import DocType
    from mod_core.annexes.models import Folder
    company = obj.company
    # import pdb; pdb.set_trace()
    mod_dataload = import_module('%s.config.dataload' % settings.SITE_NAMEX)
    data = getattr(mod_dataload, 'DATA_FOLDER')
    count = 0
    #-----------
    for data_row in data:
        alias = data_row[0]
        name = data_row[1]
        folders = data_row[2]
        count +=1
        try:
            dt = DocType.objects.get(model_name='Folder', company=company, alias=alias)
            if not obj.replace:
                continue
        except DocType.DoesNotExist:
            dt = DocType(model_name='Folder', company=company, alias=alias)
        dt.name = name
        dt.save()
        try:
            folder = Folder.objects.get(doctype=dt, alias=alias)
        except Folder.DoesNotExist:
            folder = Folder(doctype=dt, alias=alias)
        folder.name = name
        folder.sort = "%s" % count
        folder.save()
        count1 = 0
        for data1 in folders:
            count1 +=1
            try:
                folder1 = Folder.objects.get(doctype=dt, alias=data1)
            except Folder.DoesNotExist:
                folder1 = Folder(doctype=dt, alias=data1)
            folder1.name = data1
            folder1.sort = "%s_%2d" % (count, count1)
            folder1.save()




        # if params:
        #     for k,valor in params.items():
        #         setattr(folder, k, valor)
        # folder.save()


def x_load_Plan(modeladmin, request, obj):
    from django.conf import settings
    from importlib import import_module
    from mod_auth.doctypes.models import DocType
    from mod_entity.projects.models import Project
    from mod_make.plans.models import Plan, PlanFactor
    company = obj.company
    mod_dataload = import_module('%s.config.dataload' % settings.SITE_NAMEX)
    data = getattr(mod_dataload, 'DATA_PLAN')

    #-----------
    for data_row in data:
        alias = data_row[0]
        dt_alias = data_row[1]
        params = data_row[2]
        try:
            dt = DocType.objects.get(model_name='Project', company=company, alias=dt_alias)
        except DocType.DoesNotExist:
            dt = DocType(model_name='Project', company=company, alias=dt_alias)
            dt.save()
        try:
            project = Project.objects.get(doctype=dt, alias=alias)
        except Project.DoesNotExist:
            project = Project(doctype=dt, alias=alias)
        if params:
            for k,valor in params.items():
                setattr(project, k, valor)
            project.save()
        try:
            plan0 = Plan.objects.get(project=project, alias=alias)
        except Plan.DoesNotExist:
            plan0 = Plan(project=project, alias=alias)
            plan0.save()            
        try:
            factor0 = PlanFactor.objects.get(plan=plan0, alias=alias)
        except PlanFactor.DoesNotExist:
            factor0 = PlanFactor(plan=plan0, alias=alias)
            factor0.save()            
       


