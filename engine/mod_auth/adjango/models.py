from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelBase

# Create your models here.
class UserProp(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(ModelBase.Meta):
        verbose_name = _('Preferencia de Usuario')
        verbose_name_plural = _('Preferencias de Usuario')
        unique_together = ['user', 'alias']

    def default_prop(self):
        return [
            'biz', 'company'
        ]

class GroupProp(ModelBase):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta(ModelBase.Meta):
        verbose_name = _('Preferencia de Grupo')
        verbose_name_plural = _('Preferencias de Grupo')
        unique_together = ['group', 'alias']

    def default_prop(self):
        return [
            'biz', 'company'
        ]

class UserGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_user_groups'
        managed = False
        verbose_name = _('Grupo/Usuario')
        verbose_name_plural = _('Grupos/Usuarios')

    @property
    def alias(self):
        return "%s_%s" % (self.group.name, self.user.username)


    def __str__(self):
        return "%s - %s" % (self.group.name, self.user.username)
    
    def MC_user_first_name(self):
        return "%s" % self.user.first_name
    MC_user_first_name.short_description = _("Nombre y Apellidos")                        
        

class GroupPermission(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_group_permissions'
        managed = False
        verbose_name = _('Grupo/Permiso')
        verbose_name_plural = _('Grupos/Permisos')

    @property
    def alias(self):
        return "%s_%s" % (self.group.name, self.permission.name)


class UserPermission(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)

    class Meta:
        db_table = 'auth_user_user_permissions'
        managed = False
        verbose_name = _('Usuario/Permiso')
        verbose_name_plural = _('Usuarios/Permisos')

    @property
    def alias(self):
        return "%s_%s" % (self.user.username, self.permission.name)


class Migration(models.Model):
    app = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    applied = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'django_migrations'
        managed = False
        verbose_name = _('Migración')
        verbose_name_plural = _('Migraciones')
