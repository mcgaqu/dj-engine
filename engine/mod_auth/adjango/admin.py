from django.conf import settings
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from mod_admin.main1.options import ModelAdmin1, ModelLin1, ModelAuxAdmin1, ModelAuxLin1
from .models import Group, User, ContentType, Permission, LogEntry, Session, Site
from .models import  GroupProp, UserProp, UserGroup, GroupPermission, UserPermission
from mod_auth.companies.models import Menu, MenuItem
# Register your models here.

# -------
# CONTENTTYPES
#-------------------
class ContentTypeAdmin1(ModelAdmin1):
    model = ContentType
    list_display = ['app_label', 'model']
    list_filter = ['app_label']
    fields = None
    search_fields = ['app_label', 'model']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


#---------------------
# PERMISSION
#----------------------   
     
class PermissionAdmin1(ModelAuxAdmin1):
    model = Permission
    list_display = ('content_type', 'codename', 'name')
    list_filter = ('content_type__app_label',)

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False

#-----------------------------
# GROUP
#-----------------------------------
class UserGroupLin1(ModelLin1):
    model = UserGroup

class PermissionGroupLin1(ModelLin1):
    model = GroupPermission

class GroupPropLin1(ModelLin1):
    model = GroupProp
    fields = ['alias', 'name']

class MenuGroupLin1(ModelLin1):
    model = Menu
    fields = ['alias', 'name', 'active']

class GroupAdmin1(ModelAdmin1):
    model = Group
    list_display = ('id', 'name', 'AE_num_users', 'AE_num_permissions', 
                'AE_num_menuitems'
                )
    filter_horizontal = ('permissions', )
    # list_filter = ('app_label',)
    inlines = [UserGroupLin1, MenuGroupLin1, GroupPropLin1
               #  PermissionGroupLin1
                ]
    
    def AE_num_users(self, obj):
        return obj.usergroup_set.all().count()
    AE_num_users.short_description = "Nº Usuarios"
    
    def AE_num_permissions(self, obj):
        return obj.grouppermission_set.all().count()
    AE_num_permissions.short_description = "Nº Permisos"

    def AE_num_menuitems(self, obj):
        return MenuItem.objects.filter(menu__rol_menu=obj).count()
    AE_num_menuitems.short_description = "Nº Menus"

    def x__filter_actions_by_permissions(self, request, actions):
        
        dev = super()._filter_actions_by_permissions(request, actions)
        import pdb; pdb.set_trace()
        return dev
    
    def x_get_actions(self, request):
        return super().get_actions(request)

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

#------------------------------
# USER
#----------------------------

class GroupUserLin1(ModelLin1):
    model = UserGroup

class PermissionUserLin1(ModelLin1):
    model = UserPermission

class UserPropLin1(ModelLin1):
    model = UserProp
    fields = ['alias', 'name']

class MenuUserLin1(ModelLin1):
    model = Menu
    fields = ['alias', 'name']
    
class UserAdmin1(DjangoUserAdmin):
    model = User


    list_display = ('username', 'first_name', # 'last_name',
                    'email', 'is_active', 'is_staff',                   
                    'is_superuser'
                    )
    list_filter = ('groups','is_active', 'is_superuser')
    filter_horizontal = ['user_permissions' ]
    

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Identificación', {'fields': ('first_name', 'email', 'groups'),
                            # 'classes':['collapse']
                            }),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       # 'groups',
                                       'user_permissions'                                       
                                       ),
                      'classes':['collapse']
                      }),

    )

    inlines = [MenuUserLin1, UserPropLin1, 
        # GroupUserLin1, PermissionUserLin1
        ]


    def AE_num_groups(self, obj):
        return obj.usergroup_set.all().count()
    AE_num_groups.short_description = "Nº Grupos"
    
    def AE_num_permissions(self, obj):
        return obj.userpermission_set.all().count()
    AE_num_permissions.short_description = "Nº Permisos"

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True
#---------------------
    
class GroupPermissionAdmin1(ModelAdmin1):
    model = GroupPermission
    list_display = ('group', 'permission')
    
class UserPermissionAdmin1(ModelAdmin1):
    model = UserPermission
    list_display = ('user', 'permission')
    
class UserGroupAdmin1(ModelAdmin1):
    model = UserGroup
    list_display = ('user', 'group')


#------------------------------
# LogEntry
#----------------------------    
# @admin.register(LogEntry)    
class LogEntryAdmin1(ModelAdmin1):
    model = LogEntry
    list_display = ('action_time', # object_id',
                    'object_repr', # 'change_message',
                    'get_change_message',  # pasarlo a span y dibujo
                    'content_type', 'user', 'action_flag',)
    list_filter = ('action_flag', ('user', admin.RelatedOnlyFieldListFilter),
                   'content_type__app_label'
                   )
    search_fields = ('content_type__model', 'object_repr',
                    'user__username', 'change_message')
    date_hierarchy = 'action_time'

    fields = ('action_time',  'user', 
                'content_type', 'object_repr',
                'action_flag','change_message',
                )
    # readonly_fields = ('object_repr')

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

class SessionAdmin1(ModelAdmin1):
    model = Session
    
class SiteAdmin1(ModelAdmin1):
    model = Site





if settings.NUM_ADMIN_SITE == "0":
    admin.site.register(ContentType)
    admin.site.register(Permission)
    # admin.site.register(Group)
    # admin.site.register(User)
    admin.site.register(LogEntry)
    admin.site.register(Session)