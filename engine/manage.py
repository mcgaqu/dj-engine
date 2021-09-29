#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from websites import WEBSITES


def main(params):
    """Run administrative tasks."""
    # import pdb; pdb.set_trace()
    print('PARAMS MAIN: ', params)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(params)



if __name__ == '__main__':
    
    print(sys.argv)
    if (len(sys.argv) > 1) and (sys.argv[1] in WEBSITES):
        print('extraer SITE_NAME de los parámetros')
       
        SITE_NAME = sys.argv[1]
        print('websites.%s.settings' % SITE_NAME)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websites.%s.settings' % SITE_NAME)
        main([sys.argv[0]] + sys.argv[2:]) 

    elif (len(sys.argv) > 1) and (sys.argv[1] == 'engine'):
        # extraer "engine" de los parámetros
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')
        main([sys.argv[0]] + sys.argv[2:])
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')
        main(sys.argv)