from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import Group
from mod_admin.main1.options import (ModelAdmin1, ModelLin1,
                                     ModelAuxAdmin1, ModelAuxLin1,
                                     GenericLin1)

# from mod_base.configs.models import Config1, Config2
from .models import Folder, FolderAnnex


#------------------------------
# Folder
#------------------------
class FolderAnnexAdmin1(ModelAuxAdmin1):
    model = FolderAnnex
    list_display = ['docfile', 'ctt', 'obj_id', 'alias', 'name', 'grade', 'sort']
    fields = ['docfile', 'ctt', 'obj_id', 'alias', 'name', 'grade', 'sort']


class FolderAnnexLin1(GenericLin1):
    model = FolderAnnex
    ct_field = 'ctt'
    ct_fk_field = 'obj_id'
    fields = ['alias', 'name', 'grade', 'sort']


class FolderAdmin1(ModelAdmin1):
    model = Folder
    list_display = ['grade', 'sort', 'alias', 'name', 'mark', 'active', 'locked']
    list_display_links = ['grade', 'sort', 'alias', 
        # 'name', 'mark', 'active',
        'locked']
    list_editable = ['name', 'mark','active']
    list_filter = ['grade', 'sort', 'active', 'locked']
    search_fields = ['alias', 'name', 'mark']

    # fields = ['doctype','grade', 'sort', 'alias', 'name', 'mark', 'docfile', 'content',
    #      'active', 'locked', 'MH_content']
    fieldsets = [
		(None, {
			'fields': [	
                ('doctype',),
                ('grade', 'sort',),                
                ('alias', 'name'),
                ('mark', 'active', 'locked'),
				('docfile',),
                ('content'),
                ('MH_content')
            ]
		}), 
	]
    readonly_fields = ['MH_content']
    list_filter = ['grade', 'sort', 'mark', 'active', 'locked']
    search_fields = ['alias', 'name']
    # inlines = [FolderAnnexLin1, 
    # ]



if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(Folder)
    admin.site.register(FolderAnnex)

  
