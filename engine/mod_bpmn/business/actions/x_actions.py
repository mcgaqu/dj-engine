

#============================================


def load_datastate(modeladmin, request, queryset): 
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 5.- load_datastates en %s" % biz)
    print("-------------------")
    #-----------------------

def load_state(modeladmin, request, queryset):
# def load_state(modeladmin, request, queryset):
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 6.- load_states en %s" % biz)
    print("-------------------")
    #-----------------------
  
    dir_to_search = '.'
    for dirpath, dirnames, filenames in os.walk(dir_to_search):
        print(dirpath)
        for xx in (dirnames + filenames):
            # print(xx)
            # print(dirnames + filenames)
            # dpath = os.path.join(dirpath, di)
            # mod = dpath.replace('/','.')[2:]
            if xx in ['actions','actions.py']:
                # import pdb; pdb.set_trace()
                kind = xx.split('.')[0]
                dpath = os.path.join(dirpath, kind)
                mod = dpath.replace('/','.')[2:]
                modulo = import_module(mod)
                if not hasattr(modulo, 'get_app_arcos'):
                    continue
                actions = modulo.get_app_arcos()
                print('actions', actions)
                for action in actions:

                    # alias = action.__name__
                    # sort = mod
                    # if hasattr(action, 'short_description'):
                    #     name = getattr(action, 'short_description')
                    # else:
                    #     name = alias
                    alias = action
                    name = action
                    try:
                        ac = BAction.objects.get(biz=biz, alias=alias)
                    except BAction.DoesNotExist:
                        ac = BAction(biz=biz, alias=alias, name=name)
                        ac.sort = mod
                        ac.grade = kind
                        ac.locked = True
                        ac.active = False
                        ac.internal = True
                        ac.save()
    print("-----------------")
    return


#============================
# carga_ini personalizada
# ---------------------

def load_COMPANY(modeladmin, request, queryset):
    load_company1(modeladmin, request, queryset)
    load_CompanyX(modeladmin, request, queryset)
    return

def load_company1(modeladmin, request, queryset):
    biz = queryset[0]
    #-----------------
    print()
    print("BIZ 11.- load_company")
    print("-----------------")
    #-----------------------
    alias_biz = biz.alias
    #-----------------------------------------
    try:
        biz = Biz.objects.get(alias=alias_biz)
    except Biz.DoesNotExist:
        biz = Biz(alias=alias_biz)
        biz.save()
    #---------------------
    try:
        comp = Company.objects.get(alias=alias_biz, biz=biz)
    except Company.DoesNotExist:
        comp = Company(alias=alias_biz, biz=biz)
        comp.save()
    #-------------------------------
    try:
        group = Group.objects.get(name=alias_biz.upper())
    except Group.DoesNotExist:
        group = Group(name=alias_biz.upper())
        group.save()
    #-------------------------------
    try:
        rol = Rol.objects.get(alias=alias_biz.upper(), group=group, company=comp)
    except Rol.DoesNotExist:
        rol = Rol(alias=alias_biz.upper(), group=group, company=comp)
        rol.save()
    print("-----------------")
    return
 
    
def load_CompanyX(modeladmin, request, queryset):

    biz = queryset[0]
    alias_biz = biz.alias # alias_biz = settings.SITE_NAME

    # import pdb; pdb.set_trace()
    # website = os.environ['DJANGO_SETTINGS_MODULE']
    # mod_website = import_module(website)
    def get_inisettings():
        # pasar a fichero.json
        return [
            'LANGUAGE_CODE'
            ]
    companies = biz.company_set.all()
    for company in companies:

        for key in get_inisettings():
            # value = getattr(mod_website, key, '')
            value = ""
            try:
                reg = Confset.objects.get(company=company, alias=key)
            except Confset.DoesNotExist:
                reg = Confset(company=company, alias=key, name=value)
                reg.locked = True
                reg.active = False
                reg.internal = True
                reg.save()
    print("-----------------")
    return
    

def load_BizX(modeladmin, request, queryset):
    from .inidata import get_BizX
    biz = queryset[0]
    Model = BizX
    #-----------------
    print()
    print("BIZ 1.- load_BizX")
    print("-------------------")
    add = True
    #-----------------------
    if biz.locked:
        return (30, "CMS %s: bloqueado. No se puede cargar params" % biz.alias)
    args = get_BizX()
    if not args:
        return (30, "No hay params para cargar en el SITIO %s:" % biz.alias)
    #----------------
    if not biz.active:
        BizX.objects.filter(biz=biz).delete()
    else:
        BizX.objects.filter(biz=biz).update(mark='N')
    #-------------------
    count = 0
    for key, data in args.items():
        alias = key
        count +=1
        try:
            param = BizX.objects.get(biz=biz, alias=alias) # , grade=key[1])
            if not biz.replace:
                param.mark ='S'
                param.save(update_fields=['mark'])
                continue
        except BizX.DoesNotExist:
            param = BizX(biz=biz, alias=alias) # , grade=key[1])
        for attr, data1 in data.items():
            setattr(param, attr, data1)
        param.mark = 'S'
        param.date_time = timezone.now()
        param.save()
    #--------------------------------------
    BizX.objects.filter(biz=biz, mark='N').delete()
    return (25, "Biz %s: Creados %s params" % (biz.alias, count))
