import random, decimal, datetime
from django.contrib import messages
from mod_admin.utils.base import redondea, print_msg
from mod_auth.doctypes.models import DocType, get_create_doctype
from mod_entity.products.models import Product
from mod_entity.projects.models import ProjectAux
from mod_make.plans.models import Plan, PlanCV, PlanCVTax, PlanCVProduct


def get_num_factura(cv, num, patron='&&&&-#####'):
    # import pdb; pdb.set_trace()
    # patron =  cv.tipodoc.marca
    if patron == '&&&&-#####':
        return "%s-%05d" % (cv.date1.year, num)
    elif patron == '&&&&-T-#####':
        return "%s-%s-%05d" % (cv.date1.year, cv.CE_date1_trimestre, num)
    elif patron == '&&&&-T-####':
        return "%s-%s-%04d" % (cv.date1.year, cv.CE_date1_trimestre, num)
    elif patron == '######':
        return "%06d" % num
    else:
        return "%s" % num

def x_get_pesos_cvs_dia(plan_dia, cvs_dia):
    # import pdb; pdb.set_trace()
    dev = {}
    total_peso_dia_ini = [plan_dia.num_dec1, plan_dia.num_dec2, plan_dia.num_dec3]
    margen1 = 2
    margen2 = 2
    peso_fin_dia_tipo = []
    #-----------------------------
    for tipo in [1]: # ,2,3]:
        total_peso_ini = total_peso_dia_ini[tipo-1]
        peso_medio = total_peso_ini / plan_dia.num_int # ventas tipo / num ftras
        total_peso = 0
        for cv in cvs_dia:  
            #--------------------
            peso = peso_medio
            peso = peso + random.randint(-int(peso/margen1), int(peso/margen2))
            dev[cv.alias, tipo] =  peso
            total_peso +=peso
        #--------------------------
        for cv in cvs_dia:
            peso = dev[cv.alias, tipo]
            dev[cv.alias, tipo] = decimal.Decimal(peso*total_peso_ini/total_peso)
    
        # if plan_dia.num_int != total_peso:
        #     dev[cv.alias, tipo] += (plan_dia.num_int-total_num_int)
    if plan_dia.alias in ['2018T1M3D30', '2018T1M3D31']:
        import pdb; pdb.set_trace()
    return dev

def y_get_pesos_cvs_dia(plan_dia):
    # import pdb; pdb.set_trace()
    dev = {}
    total_peso_dia_ini = [plan_dia.num_dec1, plan_dia.num_dec2, plan_dia.num_dec3]
    margen1 = 2
    margen2 = 2
    # peso_fin_dia_tipo = []
    #-----------------------------
    for tipo in [1]: # ,2,3]:
        total_peso_ini = total_peso_dia_ini[tipo-1]
        peso_medio = total_peso_ini / plan_dia.num_int # ventas tipo / num ftras
        total_peso = 0
        #--------------------------
        for x in range(1, plan_dia.num_int+1):
            alias = "%s_%03d" % (plan_dia.alias, x) 
            #--------------------
            peso = peso_medio
            # peso = peso + random.randint(-int(peso/margen1), int(peso/margen2))
            # peso = peso + random.randint(-int(peso/margen1), int(peso/margen2))
            #-----------------
            dev[alias, tipo] = peso
            total_peso += peso
        #--------------------------
        total_peso_fin = 0
        for x in range(1, plan_dia.num_int+1):
            alias = "%s_%03d" % (plan_dia.alias, x)
            #-------------------- 
            peso = dev[alias, tipo]
            peso = peso*total_peso_ini/total_peso
            peso = redondea(peso, 2)
            dev[alias, tipo] = peso
            total_peso_fin += peso
        if total_peso_ini != total_peso_fin:
            dev[alias, tipo] += (total_peso_ini - total_peso_fin)
            # TODO ver si sale negativo algun importe
    # import pdb; pdb.set_trace()
    return dev

def get_pesos_cvs_dia(plan_dia):
    dev = {}
    cero = decimal.Decimal(0.0)
    # plan_dias = plan_mes.children.all()
    num_cvs_dia = plan_dia.num_int
    total_peso_dia_ini = [plan_dia.num_dec1] # , plan_dia.num_dec2, plan_dia.num_dec3]
    total_peso_dia = [0, cero]
    total_peso_dia_fin = [0, cero]
    # factor_mes = 1 if (plan_dia.date.month % 2 == 0) else -1
    # factor_dia = -1 if (plan_dia.date.day %2 == 00) else 1
    #-----------------------------
    for tipo in [0]: # 1,2]:
        total_peso_ini = total_peso_dia_ini[tipo]
        peso_medio = total_peso_ini / num_cvs_dia
        # total_peso = 0
        # signo = 1 if tipo == 0 else -1
        # factor = (plan_dia.parent.date.month() % 2) + decimal.Decimal(1.5)
        #--------------------------
        for x in range(1, num_cvs_dia+1):
            alias =  "%s_%03d" % (plan_dia.alias, x) 
            peso = peso_medio
            if False:
                signo = 1 if tipo == 0 else -1
                factor = decimal.Decimal(1.5)
                alias =  "%s_%03d" % (plan_dia.alias, x)             
                if peso > 0:
                    peso = decimal.Decimal(peso + signo*peso*factor)   
                if peso > 0:
                    peso = decimal.Decimal(peso + signo*peso*factor) 
                if peso > 0:
                    peso = decimal.Decimal(peso + signo*peso*factor)                              
            #-------------------
            dev[alias, tipo] = peso
            total_peso_dia[tipo] += peso
            # print_msg('FASE1 %s = %s' % (alias, peso))
        #--------------------------
        for x in range(1, num_cvs_dia+1):
            alias =  "%s_%03d" % (plan_dia.alias, x) 
            #-------------------- 
            peso = dev[alias, tipo]
            peso = redondea(peso*total_peso_ini/total_peso_dia[tipo],2)
            dev[alias, tipo] = peso
            total_peso_dia_fin[tipo] += peso
            # print_msg('FASE2 %s = %s' % (alias, peso))
    return dev


def generar_cvs_mes(plan_mes):
    dt = get_create_doctype(plan_mes.doctype.company, 'PlanCV')
    hijos = plan_mes.children.all() # dias
    count = 0
    for plan_dia in hijos:
        # import pdb; pdb.set_trace()
        if not plan_dia.num_int:
            continue
        # cvs_dia = PlanCV.objects.filter(doctype=dt, project=plan_mes.project, alias__startswith=plan_dia.alias)
        # pesos_dia = get_pesos_cvs_dia(plan_dia)
        for x in range(1, plan_dia.num_int+1):
            count +=1
            alias = "%s_%03d" % (plan_dia.alias, x)
            try:
                cv = PlanCV.objects.get(doctype=dt, project=plan_mes.project, alias=alias)
            except PlanCV.DoesNotExist:
                cv = PlanCV(doctype=dt, project=plan_mes.project, alias=alias)
                cv.date1 = plan_dia.date
                #-------------------
                # cv.sort = get_num_factura(cv, x, patron=None)
                # cv.grade =  "%sT%s" %  (cv.date1.year, cv.alias)
                cv.grade = cv.alias[0:6]
                cv.save()
            # import pdb; pdb.set_trace()
            # if plan_dia.num_dec1 != 0:
            #     try:
            #         cvp = PlanCVProduct.objects.get(cv=cv, alias='Venta_tipo1')
            #     except PlanCVProduct.DoesNotExist:
            #         cvp = PlanCVProduct(cvc=cv, alias='Venta_tipo1')
            #     cvp.units = pesos_dia[cv.alias, 0]
            #     cvp.porc_tax = decimal.Decimal(plan_dia.num_int1) 
            #     cvp.price = 1
            #     cvp.save()
            # if plan_dia.num_dec2 != 0:
            #     try:
            #         cvp = PlanCVProduct.objects.get(cv=cv, alias='Venta_tipo2')
            #     except PlanCVProduct.DoesNotExist:
            #         cvp = PlanCVProduct(cv=cv, alias='Venta_tipo2')
            #     cvp.units = pesos_dia[cv.alias, 2]
            #     cvp.porc_tax = decimal.Decimal(plan_dia.num_int2)
            #     cvp.price = 1
            #     cvp.save()
            # cv.save_tax()
            # cv.save()
    return "%s de %s" % (count, plan_mes.num_int)




def x_generar_cvproducto_mes(cvmes):
    dict_productos = {}
    # seleccionar productos tasa 1/2/3 de projectaux y calcular peso total
    # para cada producto
    #   calcular peso real de cada producto en unidades con respecto 
    #   al importe total del tipo y el precio
    #   dict_productos[producto] = [uds_totales (decimal), varacion ]           +
    #-----------------------
    #   distribuir las unidades en unidades+-variacion
    #   y crear plancvproduct correspondientes asignados al mes (no tiene CV todavia)
    #   OJO con la última unidad habrá que reasignarla si no encaja
    #   hasta aquí lineas de productos se corresponden con las ventas del mes
    #------------------------------------------------   
    # TODO !!! mejora: intercambio de productos en el mes sin alterar el importe 
    #              --> estacionidad de productos
    # ======================
    # distribucion en dias/facturas



def generar_cvproducto_mes(cvmes):
    return
    def get_productos(project, grupo, tasa):
        # import pdb; pdb.set_trace()
        productos = ProjectAux.objects.filter(trunk=project, inline='TARIFA', grade=grupo, mark=tasa)
        # productos = Product.objects.filter(tipodoc__alias=ejercicio,
        # grupo=grupo, activo=True, tasa=tasa)
        lista_productos = []
        for p in productos:
            lista_productos += [p for x in range(1, p.num_int)]
        margen = len(lista_productos)-1
        if margen < 0:
            print("ERROR: NO TENGO PRODUCTOS %s de tasa %s" % (grupo, cvmes_plin.tasa.nombre))
            return ([], 0)
        print("ejercicio = %s, grupo=%s, tasa=%s" % (project.alias, grupo, tasa))
        print("Productos=%s, lista_productos=%s" % (productos.count(), len(lista_productos)))
        return (lista_productos, margen)

    def graba_cvp(lista_productos, margen, cvmes_plin, cv, resto_mes, lin=0):
        producto = lista_productos[random.randint(0, margen)]
        # precio_base = producto.precio_ingreso/(1+cvmes_plin.tasa.porc/100)
        precio_base = producto.num_dec/(1+cvmes_plin.tasa.porc/100)
        
        # import pdb; pdb.set_trace()
        if producto.orden and producto.orden.isdigit():
            mg1 = int(producto.orden)*100
            # precio_base = precio_base*(1 + 1/100*random.randint(-mg1,mg1))
            precio_base += decimal.Decimal(random.randint(-mg1,mg1)/100)
        precio_base = redondea(precio_base, 4)
        if resto_mes < precio_base:
            precio_base = resto_mes
            precio = redondea(precio_base + precio_base*cvmes_plin.tasa.porc/100,4)
        else:
            if producto.orden and producto.orden.isdigit():
                precio = redondea(precio_base + precio_base*cvmes_plin.tasa.porc/100,4)
            else:
                precio = producto.precio_ingreso
        #-----------------------
        if not lin:
            lin = cv.cvproducto_set.count()+1
        #---------------
        try:
            cvp = PlanCVProduct.objects.get(cv=cv,lin=lin)
        except PlanCVProduct.DoesNotExist:
            cvp = PlanCVProduct(cv=cv, lin=lin)
        cvp.producto = producto
        cvp.unidades = 1
        #--------------------
        cvp.tasa = cvmes_plin.tasa
        cvp.iva_incluido = True # ojo en los calculos con los ivas
        cvp.precio = precio
        #-----------------
        cvp.entero = cv.tipodoc.id
        cvp.save()
        return precio_base

    #-------------------------
    # Distribuir las bases imponibles del mes en las facturas generadas
    #--------------------------------------
    print_msg("Generando lin=1 de cvs del mes %s. %s" % (cvmes.alias,
                    datetime.datetime.now().strftime("%H:%M")))
    
    cvs = PlanCV.objects.filter(alias__startswith=cvmes.alias, internal=False)
    #----------------------
    # TODO !!! Paso 1 : completar las facturas fijas X
    #--------------------
    cvxs = PlanCV.objects.filter(alias__startswith=cvmes.alias, internal=True, grade="X")
    if cvxs.count():
        for cvx in cvxs:
            try:
                cve = cvs.objects.get(orden=cvx.orden)
                for cvpx in cvx.plancvproduct_set.all():
                    cvpx.id = None
                    cvpx.cv = cve
                    cvpx.internal = False
                    cvpx.locked = True
                    cvpx.save()
                cve.save()
            except PlanCV.DoesNotExist:
                pass

    #---------------------
    # Fila 1 del mes
    #-------------------
    plan_mes = cvmes
    cvmes_plin = cvmes.cvproducto_set.get(lin=1)
    grupo = "B"
    lista_productos, margen = get_productos(
        cvmes.tipodoc.alias, grupo, cvmes_plin.tasa.padre)
    if lista_productos:
        #---------------------
        resto_mes = cvmes_plin.importe_base
        conta = 0
        lin = 1
        #-----------------------
        # Fila 1 del mes y fila 1 de facturas
        #----------------------------
        for cv in cvs:
            conta +=1
            if cv.bloqueado: # cv.grupo == 'X'
                resto_mes -= cv.cvproducto_set.get(lin=lin).importe_base
            else:
                #-------------------------
                # import pdb; pdb.set_trace()
                resto_mes -= graba_cvp(lista_productos, margen, cvmes_plin, cv, resto_mes, lin=1)
            if resto_mes <= 0:
                break
        #--------------------------
        cvs1 = []
        if conta < cvs.count():
            print_msg("ERROR: Me quedan %s facturas de %s sin fila 1 en el mes %s. %s" % (
                        cvs.count()-conta, cvs.count(), cvmes.alias,
                        datetime.datetime.now().strftime("%H:%M")))
            cvs1 = list(cvs.filter(total_base=0))
        if resto_mes > 0: 
            print_msg("Me sobra %s de la fila 1 (%s) para distribuir. %s" % (
                        resto_mes, cvmes_plin.importe_base,
                        datetime.datetime.now().strftime("%H:%M")))
            #-----------------------
            # Fila 1 del mes y filas >1 de facturas
            #----------------------------
            cvs1 = list(cvs)
            grupo = "B"
            #----------------------
            lista_productos, margen = get_productos(
                cvmes.tipodoc.alias, grupo, cvmes_plin.tasa.padre)
            conta = 0
            while resto_mes > 0:
                if not cvs1:
                    cvs1 = list(cvs)
                    # lin += 1
                #-----------------------
                j = random.randint(0, len(cvs1)-1)
                cv = cvs1[j]
                del cvs1[j]
                #-------------------
                conta +=1
                if cv.bloqueado: # cv.grupo == 'X'
                    resto_mes -= cv.cvproducto_set.get(lin=lin).importe_base
                else:
                    #-------------------------
                    resto_mes -= graba_cvp(lista_productos, margen, cvmes_plin, cv, resto_mes)
    #-------------------------
    # Filas >1 del mes y filas >1 de facturas
    #----------------------------
    # import pdb; pdb.set_trace()
    try:
        grupo = "C"
        cvmes_plin = cvmes.cvproducto_set.get(lin=2)
        #-----------------------
        lista_productos, margen = get_productos(
            cvmes.tipodoc.alias, grupo, cvmes_plin.tasa.padre)
        resto_mes = cvmes_plin.importe_base
        # cvs1 = []
        while resto_mes > 0:
            if not cvs1:
                cvs1 = list(cvs)
                lin += 1
            #-----------------------
            j = random.randint(0, len(cvs1)-1)
            cv = cvs1[j]
            del cvs1[j]
            #-------------------
            conta +=1
            if cv.bloqueado: # cv.grupo == 'X'
                resto_mes -= cv.cvproducto_set.get(lin=lin).importe_base
            else:
                #-------------------------
                resto_mes -= graba_cvp(lista_productos, margen, cvmes_plin, cv, resto_mes)
    except PlanCVProduct.DoesNotExist:
        pass
    #--------------------------
    print_msg("Fase4: Regrabar %s facturas generadas. %s" % (
                    cvs.count(),datetime.datetime.now().strftime("%H:%M")))
    for cv in cvs:
        cv.save()
        cv.save_tasa()
        
    #------------------------
    print_msg("FIN Generando cvs del mes %s. %s" % (cvmes.alias,
                    datetime.datetime.now().strftime("%H:%M")))
    return cvs.count()     

def x_renumerar_cvs(plan):
    obj = plan
    # ejercicio = obj.project.alias
    year = plan.alias
    patron = obj.patron_alias or ""
    for plan in Plan.objects.filter(alias__startswith=plan.alias, level=1).order_by('alias'):
        num = 0
        cvs = PlanCV.objects.filter(alias__startswith=plan.alias, internal=False).order_by('alias')
        for cv in cvs:
            num +=1
            # cv.sort = get_num_factura(cv, num, patron="")
            cv.sort = "%s-%05d" % (cv.date1.year, num)
            cv.save(update_fields=['sort'])
    return

def ac_generate_plancvs(modeladmin, request, queryset, pieza=None):
    count = 0
    for plan in queryset:
        if not plan.locked or not plan.internal:
            mensaje = "Plan %s debe ser locked y internal para calcular" % plan.alias
            modeladmin.message_user(request, mensaje, messages.WARNING)
            continue

        count +=1
        # generate_plancvs(plan)
        #------------------------------
        # borrar calculo anterior
        #-------------------------------------
        obj = plan
        PlanCVTax.objects.filter(cv__alias__startswith=obj.alias,
                cv__internal=False).delete()
        PlanCVProduct.objects.filter(cv__alias__startswith=obj.alias,
                cv__internal=False).delete()
        PlanCV.objects.filter(alias__startswith=obj.alias,
                internal=False).delete()      
        #----------------------------------
        if obj.level == 0:
            for cv_trimestre in obj.children.all():
                for cv_mes in cv_trimestre.children.all():
                    num_cvs = generar_cvs_mes(cv_mes)
                    mensaje = "%s: facturas generadas = %s" % (cv_mes.alias, num_cvs)
                    modeladmin.message_user(request, mensaje)
                    num_cvs = generar_cvproducto_mes(cv_mes)
                    mensaje = "%s: detalle facturas generadas = %s" % (cv_mes.alias, num_cvs)
                    modeladmin.message_user(request, mensaje)
        elif obj.level == 1:
            for cv_mes in obj.children.all():
                num_cvs = generar_cvs_mes(cv_mes)
                mensaje = "%s: facturas generadas = %s" % (cv_mes.alias, num_cvs)
                modeladmin.message_user(request, mensaje)
                num_cvs = generar_cvproducto_mes(cv_mes)
                mensaje = "%s: detalle facturas generadas = %s" % (cv_mes.alias, num_cvs)
                modeladmin.message_user(request, mensaje)
        elif obj.level == 2:
            num_cvs = generar_cvs_mes(obj)
            mensaje = "%s: facturas generadas = %s" % (obj.alias, num_cvs)
            modeladmin.message_user(request, mensaje)
            num_cvs = generar_cvproducto_mes(obj)
            mensaje = "%s: detalle facturas generadas = %s" % (obj.alias, num_cvs)
            modeladmin.message_user(request, mensaje)
        mensaje = "Se han calculado el ejercicios %s" % (plan.alias)
        modeladmin.message_user(request,mensaje, messages.SUCCESS)
        #---------------------------
        # Comprobar si hay facturas 0, si hay borrarlas y renumerar el año ???
        #--------------------------------
        if False:
            cvs0 = PlanCV.objects.filter(alias__startswith=obj.alias, internal=False, amount_total=0)
            num_cvs0 = cvs0.count()
            if num_cvs0:
                cvs0.delete()
    #--------------------------------
    # if False: # num_cvs0
    #     renumerar_facturas(plan)

    return
ac_generate_plancvs.short_description = "2.- Generar Facturas/Dias"

def ac_renumerar_cvs(modeladmin, request, queryset, pieza=None):
    plan_year = queryset[0]
    if queryset.count() > 1 or plan_year.level != 0:
        mensaje = "Solo se puede renumerar un ejercicio completo. Plan %s no válido" % plan_year.alias
        modeladmin.message_user(request, mensaje, messages.WARNING)
        return
    
    # renumerar_facturas(plan)
    year = plan_year.alias
    patron = plan_year.patron_alias or ""
    cvs = PlanCV.objects.filter(alias__startswith=year, internal=False).order_by('alias')
    num = 0
    for cv in cvs:
        num +=1
        # cv.sort = get_num_factura(cv, num, patron="")
        cv.sort = "%s-%05d" % (year, num)
        cv.save(update_fields=['sort'])
    mensaje = "Renumeradas %s cvs" % num
    modeladmin.message_user(request, mensaje, messages.SUCCESS)
    return
ac_renumerar_cvs.short_description = "3.- Renumerar Facturas"