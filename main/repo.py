from .models import Customer


class Repo:
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def get_by_id(self, id_):
        return self._get_model_obj_by_id(id_).to_dto()

    def get_all(self):
        return tuple(obj.to_dto() for obj in self.model_cls.objects.all().order_by('pk'))

    def create(self, **kwargs):
        model_obj = self.model_cls()
        for attr, value in kwargs.items():
            if not hasattr(model_obj, attr):
                raise self.InvalidAttribute()
            elif value is not None:
                setattr(model_obj, attr, value)
        model_obj.save()
        return model_obj.to_dto()
    
    def delete(self, id_):
        try:
            self.model_cls.objects.get(id=id_).delete()
        except self.model_cls.DoesNotExist:
            raise self.DoesNotExist()

    class DoesNotExist(Exception):
            pass
    class InvalidAttribute(Exception):
        pass

class CustomerRepo(Repo):
    def __init__(self):
        super().__init__(Customer)

    def get_all(self, **kwargs):
        return super().get_all(**kwargs)

    def get_by_id(self, user_id, **kwargs):
        return super().get_by_id(user_id, **kwargs)
    
    def create(self,country, **kwargs):
        model_obj = self.model_cls()
        grade = model_obj.getGradeKey(country)
        return super().create(grade=grade,**kwargs)

    def delete(self, id):
        return super().delete(id)
    #TODO
    def bulk_create(self, **kwargs):
        return