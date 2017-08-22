from django.db.models import Count


class CrudRepo(object):
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def get_query_set(self):
        return self.model_cls.objects.all()

    def get_list(self, offset, limit, **kwargs):
        qset = self.get_query_set()
        return list(qset.filter(**kwargs)[offset: limit])

    def get_object(self, default=None, **kwargs):
        qset = self.get_query_set()
        try:
            return qset.get(**kwargs)
        except self.model_cls.DoesNotExist:
            return default

    def get_count(self, **kwargs):
        qset = self.get_query_set()
        return qset.filter(**kwargs).count()

    def create(self, **kwargs):
        obj = self.model_cls.create(**kwargs)
        return obj

    def delete(self, obj):
        obj.delete()
        return obj

    def update(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def aggregates(self, **args):
        qset = self.get_query_set()
        qset = qset.values(*args)
        return qset.annotate(count=Count('id'))
