import calendar, datetime, decimal
from django.conf import settings



def print_msg(msg):
    # if settings.DEBUG:
    print(msg)
    return

def redondea(numero, redondeo=2, tipo=None, empresa=None):
    if not numero and numero != 0:
        numero = 0
        
    try:
        numero = decimal.Decimal(str(numero))
    except:
        numero = decimal.Decimal(0)
    
    if tipo in ('unidades', 'precios', 'importes',):
        pass
        # redondeo = decimales_parametro_empresa(tipo, empresa)
    elif tipo and tipo.isdigit():
        # el tipo puede llevar el numero de decimales
        redondeo = int(tipo)
    return numero.quantize(decimal.Decimal(10)**(-redondeo), decimal.ROUND_HALF_UP)


def get_dates_from_period(period):
    year = period[0:4]
    if 'D' in period:
        month1 = int(period[7:9])
        month2 = month1
        day1 = int(period[10:12])
        day2 = day1
    elif 'M' in period:
        month1 = int(period[7:9])
        month2 = month1
        day1 = 1
        day2 = calendar.monthrange(year, month2)[1]
    elif 'T' in period:
        trimester = int(period[5:6])
        month1 = (trimester-1)*3 +1
        day1 = 1
        month2 = month1+2
        day2 = calendar.monthrange(year, month2)[1]
    else:
        month1 = 1
        day1 = 1
        month2 = 12
        day2 = 31
    date1 = datetime.date(year, month1, day1)
    date2 = datetime.date(year, month2, day2)
    return (date1, date2)




def get_apirest_fields(model):
    # import pdb; pdb.set_trace()
    fields = model._meta.concrete_fields
    # dev = [x.name for x in fields]
    dev = ['id', 'url']
    for field in fields:
        dev.append(field.name)
        if field.many_to_one:
            dev.append("%s_id" % field.name)# dev.append(field.name)
        # print(field.name)
    # print(dev)
    return dev
