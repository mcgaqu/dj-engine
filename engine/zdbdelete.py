# -*- coding: utf-8 -*-

import os
import sys
from mod_admin.utils.databases import dbsite_delete
from websites import WEBSITES
# ---------------------------
if __name__ == '__main__':
    print(sys.argv)
    if (len(sys.argv) > 1) and (sys.argv[1] in WEBSITES):
        SITE_NAME = sys.argv[1]
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websites.%s.settings' % SITE_NAME)
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')
    dbsite_delete()
