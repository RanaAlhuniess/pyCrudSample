from django.db import models
from django.contrib.auth.models import User
from .dto import EmployeeDTO


class Employee(models.Model):
    account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="account"
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dto(self):
        return EmployeeDTO(self.id, self.birthday, self.creator, self.account)

