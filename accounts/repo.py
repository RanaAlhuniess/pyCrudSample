from django.contrib.auth.models import User
from .models import Employee


class Repo:
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def create(self, **kwargs):
        model_obj = self.model_cls()
        print(model_obj)
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


class UserRepo(Repo):
    def __init__(self):
        super().__init__(User)

    def delete(self, id):
        return super().delete(id)


class EmployeeRepo(Repo):
    def __init__(self):
        super().__init__(Employee)

    def update_or_create(self, user, dob):
        return Employee.objects.update_or_create(account=user,
                                                 defaults={'creator': user, 'birthday': dob})
    def create(self, user):
        return Employee.objects.create(account=user,creator=user)