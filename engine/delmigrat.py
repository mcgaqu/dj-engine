# import os,sys,re
import sys
from mod_admin.utils.databases import delete_migrations

# Boorar ficheros de migrations
# dir_to_search = ".engine"
# dir_to_search = ".websites.site01"

def delete_migrat (desde='2', dir_to_search='.'):
    delete_migrations(desde='2', dir_to_search='.')
    

if __name__ == '__main__':
    if (len(sys.argv) > 2):
        delete_migrations(sys.argv[1], sys.argv[2])
    elif (len(sys.argv) > 1):
        delete_migrations(sys.argv[1])
    else:
        delete_migrations()
