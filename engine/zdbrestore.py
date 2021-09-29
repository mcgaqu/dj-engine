# -*- coding: utf-8 -*-

import os
import sys
from mod_admin.utils.databases import db_restore
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = os.path.basename(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % SITE_NAME


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        db_restore(sys.argv[1])
    else:
        db_restore()
