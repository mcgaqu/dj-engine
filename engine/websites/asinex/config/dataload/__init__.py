
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
    ['websites.asinex.config.dataload', 'load_Folder', 'Cargar Folders: DocType + Folder', {},],
    

]

#========================
DATA_COMPANY = {
    'name': 'ASINEX, Legal & TAX CONSULTANCY',
    'tin':'B18521971', 
    'address': 'Av. Juan Carlos I, 24, Bajo. Edif. OMEYA',
    'zipcode': '18690',
    'city': 'Almuñecar - GRANADA',
    'state': "España",
    'tel': '958 63 18 55',
    'email': 'info@asinex.es'
}



#---------------------
DATA_COMPANYPROP = [

]

def load_Folder(modeladmin, request, obj):
    from django.conf import settings
    from importlib import import_module
    from mod_auth.doctypes.models import DocType
    from mod_core.annexes.models import Folder
    from .dataload1 import get_DATA_FOLDER
    company = obj.company
    try:
        dt = DocType.objects.get(model_name='Folder', company=company, alias='Folder')
    except DocType.DoesNotExist:
        dt = DocType(model_name='Folder', company=company, alias='Folder')
        dt.name = 'Folder'
        dt.save()
    data = get_DATA_FOLDER()
    count = 0
    #-----------
    for data_row in data:
        # grade = "%s_%s" % (data_row[0], data_row[1])
        grade = data_row[0]
        folders = data_row[2]
        count +=1
        count1 = 0
        for data1 in folders:
            name = data1[0]
            params = data1[1]
            count1 +=1
            sort = "%02d" % (count1)
            alias1 = "%s_%s" % (data_row[0], sort)
            try:
                folder1 = Folder.objects.get(doctype=dt, grade=grade, sort=sort)
            except Folder.DoesNotExist:
                folder1 = Folder(doctype=dt, grade=grade, sort=sort)
            folder1.alias = alias1
            folder1.name = name
            folder1.sort = sort
            # folder1.mark = sort
            if params:
                for k,valor in params.items():
                    setattr(folder1, k, valor)
            folder1.save()
    return

def x_load_Folder(modeladmin, request, obj):
    from django.conf import settings
    from importlib import import_module
    from mod_auth.doctypes.models import DocType
    from mod_core.annexes.models import Folder
    from .dataload1 import get_DATA_FOLDER
    company = obj.company
    # import pdb; pdb.set_trace()
    # mod_dataload = import_module('%s.config.dataload' % settings.SITE_NAMEX)
    # data = getattr(mod_dataload, 'DATA_FOLDER')
    data = get_DATA_FOLDER()
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
        folder.grade = alias
        folder.sort = "%s" % count
        folder.save()
        count1 = 0
        for data1 in folders:
            alias1 = data1[0]
            params = data1[1]
            count1 +=1
            try:
                folder1 = Folder.objects.get(parent=folder, alias=alias1)
            except Folder.DoesNotExist:
                folder1 = Folder(parent=folder, alias=alias1)
            folder1.name = alias1
            folder1.grade = alias
            # folder1.parent = folder
            folder1.sort = "%s_%02d" % (count, count1)
            if params:
                for k,valor in params.items():
                    setattr(folder, k, valor)
            folder1.save()
    return