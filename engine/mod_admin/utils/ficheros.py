# -*- coding: utf-8 -*-


import os
from django.conf import settings

def get_carpeta_instal(instal=settings.SITE_NAME):
    site_name = settings.SITE_NAME
    carpeta = settings.DATA_ROOT
    try:
        os.mkdir(carpeta)
    except:
        pass
    return carpeta


def get_carpeta_media(subcarpeta=''):
    site_name = settings.SITE_NAME
    carpeta = get_carpeta_instal()
    for nombre in ('%s_media' % site_name, subcarpeta):
        if nombre:
            carpeta = os.path.join(carpeta, nombre)
            try:
                os.mkdir(carpeta)
            except:
                pass
    return carpeta

def get_carpeta_temp(subcarpeta=''):
    site_name = settings.SITE_NAME
    carpeta = get_carpeta_instal()
    for nombre in ('%s_media' % site_name, 'temp', subcarpeta):
        if nombre:
            carpeta = os.path.join(carpeta, nombre)
            try:
                os.mkdir(carpeta)
            except:
                pass
    return carpeta


def get_carpeta_temp_user(username):
    site_name = settings.SITE_NAME
    carpeta_path = get_carpeta_instal()
    for nombre in ('%s_media' % site_name, 'temp', username):
        carpeta_path = os.path.join(carpeta_path, nombre)
        try:
            os.mkdir(carpeta_path)
        except:
            pass
    # carpeta_url = "%s%stemp/%s" % ("", # settings.PREFIJO_MEDIA_URL,
    #                                settings.MEDIA_URL, username)
    carpeta_url = "%stemp/%s" % (settings.MEDIA_URL, username)
    return (carpeta_path, carpeta_url)
