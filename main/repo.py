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
    
    # def createBulk(self, list):
    #     model_obj = self.model_cls()
    #     for attr, value in kwargs.items():
    #         if not hasattr(model_obj, attr):
    #             raise self.InvalidAttribute()
    #         elif value is not None:
    #             setattr(model_obj, attr, value)
    #     model_obj.save()
    #     return model_obj.to_dto()

class CustomerRepo(Repo):
    def __init__(self):
        super().__init__(Customer)

    def get_all(self, **kwargs):
        return super().get_all(**kwargs)

    def get_by_id(self, user_id, **kwargs):
        return super().get_by_id(user_id, **kwargs)
    
    def create(self, **kwargs):
        return super().create(**kwargs)

    def bulk_create(self, **kwargs):
        return
