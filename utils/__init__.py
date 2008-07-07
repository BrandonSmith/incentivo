from django.db import models

class UUIDField(models.CharField):

    def __init__(self, name=None, verbose_name=None, auto=True, **kwargs):
        self.auto = auto
        kwargs['max_length'] = 8
        if auto:
            kwargs['blank'] = True
            kwargs['editable'] = False
        models.CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return models.CharField.__name__

    def pre_save(self, model_instance, add):
        if add and self.auto:
            try:
                from django.utils import uuid
            except ImportError:
                import uuid
                
            while True:
                value = unicode(uuid.uuid1()).partition('-')[0]
                try:
                    self.cls.objects.get(pk=value)
                except self.cls.DoesNotExist:
                    break;
                   
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(UUIDField, self).pre_save(model_instance, add)

    def contribute_to_class(self, cls, name):
        self.cls = cls
        models.CharField.contribute_to_class(self, cls, name)

