
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from mod_admin.models.modelbase import ModelBase, ModelAuxBase
from mod_bpmn.business.models import Biz
# Create your models here.

def get_app_models():
    return [
        BAction,
        BReducer,
        # BStore
    ]

class BAction(ModelBase):
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    # alias "FACTURAR_ALBARAN", "BLOQUEAR_REGISTROS"
    # tags: parámetros separadas por coma
    # json: diccionario de salida

    def get_json(self):
        dev = {}
        dev['type']= self.alias
        params = self.tags.split(',')
        for param in params:
            dev[param] = param
        return dev

    def save(self, *args, **kwargs):
        self.json = self.get_json()
        return super().save(*args,**kwargs) 


    class Meta(ModelBase.Meta):
        verbose_name = 'Action'
        verbose_name_plural = 'Actionss'
        unique_together= (('biz','alias'),)


class BReducer(ModelBase):
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    class Meta(ModelBase.Meta):
        verbose_name = 'Reducer'
        verbose_name_plural = 'Reducers'
        unique_together= (('biz','alias'),)

#------------------
class BStoreManager(models.Manager):
    use_in_migrations = True

    def dispatch(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
        return self.model.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=str(object_id),
            object_repr=object_repr[:200],
            action_flag=action_flag,
            change_message=change_message,
        )

class BStore(ModelBase):
    biz = models.ForeignKey(Biz, on_delete=models.CASCADE, 
                                    null=True, blank=True)
    class Meta(ModelBase.Meta):
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        unique_together= (('biz','alias'),)

"""
class BStore(ModelBase):
    # action_time = models.DateTimeField(
    #     _('action time'),
    #     default=timezone.now,
    #     editable=False,
    # )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
    )
    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        verbose_name=_('content type'),
        blank=True, null=True,
    )
    object_id = models.TextField(_('object id'), blank=True, null=True)
    # Translators: 'repr' means representation (https://docs.python.org/library/functions.html#repr)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_('action flag'), choices=ACTION_FLAG_CHOICES)
    # change_message is either a string or a JSON structure
    change_message = models.TextField(_('change message'), blank=True)

    objects = BStoreManager()

    class Meta:
        verbose_name = _('BStore')
        verbose_name_plural = _('BStores')
        # db_table = 'django_admin_log'
        ordering = ['-date_time']

    def __repr__(self):
        return str(self.action_time)

    def __str__(self):
        if self.is_addition():
            return gettext('Added “%(object)s”.') % {'object': self.object_repr}
        elif self.is_change():
            return gettext('Changed “%(object)s” — %(changes)s') % {
                'object': self.object_repr,
                'changes': self.get_change_message(),
            }
        elif self.is_deletion():
            return gettext('Deleted “%(object)s.”') % {'object': self.object_repr}

        return gettext('LogEntry Object')

    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION

    def get_change_message(self):
        
        # If self.change_message is a JSON structure, interpret it as a change
        # string, properly translated.
        
        if self.change_message and self.change_message[0] == '[':
            try:
                change_message = json.loads(self.change_message)
            except json.JSONDecodeError:
                return self.change_message
            messages = []
            for sub_message in change_message:
                if 'added' in sub_message:
                    if sub_message['added']:
                        sub_message['added']['name'] = gettext(sub_message['added']['name'])
                        messages.append(gettext('Added {name} “{object}”.').format(**sub_message['added']))
                    else:
                        messages.append(gettext('Added.'))

                elif 'changed' in sub_message:
                    sub_message['changed']['fields'] = get_text_list(
                        [gettext(field_name) for field_name in sub_message['changed']['fields']], gettext('and')
                    )
                    if 'name' in sub_message['changed']:
                        sub_message['changed']['name'] = gettext(sub_message['changed']['name'])
                        messages.append(gettext('Changed {fields} for {name} “{object}”.').format(
                            **sub_message['changed']
                        ))
                    else:
                        messages.append(gettext('Changed {fields}.').format(**sub_message['changed']))

                elif 'deleted' in sub_message:
                    sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                    messages.append(gettext('Deleted {name} “{object}”.').format(**sub_message['deleted']))

            change_message = ' '.join(msg[0].upper() + msg[1:] for msg in messages)
            return change_message or gettext('No fields changed.')
        else:
            return self.change_message

    def get_edited_object(self):
        # Return the edited object represented by this log entry.
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def get_admin_url(self):
        
        # Return the admin URL to edit the object represented by this log entry.
        
        if self.content_type and self.object_id:
            url_name = 'admin:%s_%s_change' % (self.content_type.app_label, self.content_type.model)
            try:
                return reverse(url_name, args=(quote(self.object_id),))
            except NoReverseMatch:
                pass
        return None
"""