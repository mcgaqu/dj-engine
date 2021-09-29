# -*- coding: utf-8 -*-

import os
import sys
from mod_admin.utils.databases import db_backup
# from websites import WEBSITES
# ---------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
site_name = os.path.basename(base_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % site_name


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        db_backup(sys.argv[1])
    else:
        db_backup()
