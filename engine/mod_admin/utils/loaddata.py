# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

def load_datamodel(Model, data=None, replace=False, add=True):

    if not data:
        return "No hay datos para cargar"
    # import pdb; pdb.set_trace()
    count = 0
    datax = {}
    for key1, data1 in data.items(): # six.iteritems(params):
        count += 1
        try:
            param = Model.objects.get(alias=key1)
            if not replace:
                param.mark ='S'
                param.save(update_fields=['mark'])
                # param.save() # (update_fields=['marca',])
                continue
        except Model.DoesNotExist:
            if not add:
                continue
            param = Model(alias=key1)
            param.save()
        param.mark = 'S'
        param.date_time = timezone.now()
        param.internal = True
        #---------------------------------
        for attr, value in data1.items():
            if attr == 'datax_set':
                datax.update({attr:value})
            elif attr.startswith('FK__'):
                FK_attr = attr.split('__')[1]
                FK_model = ContentType.objects.get(
                    app_label=value[0][0], model=value[0][1]).model_class()
                FK_filter = value[1]
                try:
                    # fk = FK_model.objects.get(alias=value)
                    fk = FK_model.objects.get(**FK_filter)
                except FK_model.DoesNotExist:
                    import pdb; pdb.set_trace()
                    print("No existe el registro relacionado %s: %s" % (attr, value))
                    continue
                setattr(param, FK_attr, fk)
            else:
                setattr(param, attr, value)
        param.save()
    mensaje = "Cargados %s registros" % count
    #------------------------------------
    if datax:
        mensaje += load_datamodelx(Model, datax, replace, add)
    return mensaje


def load_datamodelx(Model, data=None, replace=False, add=True):
    try:
        ModelX = ContentType.objects.get(
                app_label=Model._meta.app_label,
                model = "%sx" % Model.__name__.lower()).model_class()
    except ContentType.DoesNotExist:
        return "No existe el Modelo a cargar %s" % ModelX.__name__
    
    for key1, data1 in data.items(): # six.iteritems(params):
        count = 0
        if data1.get('datax_set', {}):
            count += 1
            trunk = Model.objects.get(alias=key1)
            for key2, data2 in data1.get('datax_set', {}).items(): # six.iteritems(params):
                try:
                    param = ModelX.objects.get(trunk=trunk, alias=key2)
                    if not replace:
                        param.mark ='S'
                        param.update_fields(['mark'])
                        # param.save() # (update_fields=['marca',])
                        continue
                except ModelX.DoesNotExist:
                    param = ModelX(trunk=trunk, alias=key2)
                    param.sort = "%s_%02d" % (trunk.sort, count)
                param.mark = 'S'
                param.date_time = timezone.now()
                param.internal = True
                #--------------------------
                # if 'campox' in data2.keys():
                #     #----------------------
                #     # No se permiten campos extra que no estén previamente cargados desde código
                #     # Los datosx con campox son campos internos que tendrán funcionalidad propia
                #     # Sin campox son datos de información suplementaria sin funcionalidad específica
                #     #----------------------------
                #     try:
                #         cex = ExtraCampo.objectcs.get(alias=data2['campox'])
                #         data2['campox'] = cex
                #     except ExtraCampo.DoesNotExist:
                #         del(data2['campox'])
                # for attr, valor in data2.items():
                #     setattr(param, attr, valor)
                # param.save()
    return " Cargados %s datox_set" % count

#----------------------
