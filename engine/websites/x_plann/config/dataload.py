
#-----------
# Company
#--------------
DATA_LOAD = [
 
    ['mod_auth.companies.actions', 'load_Company', 'Cargar Company', {}],
    ['mod_auth.companies.actions', 'load_CompanyProp', 'Cargar Company Props', {}],
    ['mod_auth.companies.actions', 'load_rols', 'Cargar Rols', {}],
    ['mod_auth.companies.actions', 'load_general_menu', 'Cargar General Menu', {}],
    ['mod_auth.companies.actions', 'load_rol_menus', 'Cargar Rol Menus', {}],
    ['websites.myplan.config.dataload', 'load_Plan', 'Cargar PLANS: Project + DocType', {},],
   # ['engine.config.dataload', 'load_Plan', 'Cargar PLANS: Project + DocType', {},],
    #-----------------------
    # ['mod_auth.companies', 'load_Plan', 'Cargar DocType', {'model': 'DocType'}]
]


#========================
DATA_COMPANY = {
    'name': 'Software Integrado para el control de Empresa, S.L.',
    'tin':'B18521971', 
    'state': "España"
}



#---------------------
DATA_COMPANYPROP = [

]
#---------------
DATA_PLAN = [
    ['JN', 'PLAN', {
        'name': 'Jamones Nicolás',
        'tin':'B11111111', 
        'state': "España"
    }],
    ['PeluRosi','PLAN',  {
        'name': 'Peluquería Rosi',
        'tin':'B22222222', 
        'state': "España"
    }],
    ['Pruebas', 'PLAN', {
        'name': 'Software Integrado para el control de Empresa, S.L.',
        'tin':'B18521971', 
        'state': "España"
    }]
]

def load_Plan(modeladmin, request, obj):
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
       

