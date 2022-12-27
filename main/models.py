from django.db import models
from django.contrib.auth.models import User
from .dto import CustomerDTO


class CustomerGrade(models.Model):
    country = models.CharField(max_length=200)


class Customer(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.ForeignKey(CustomerGrade, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birthday = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def to_dto(self):
        return CustomerDTO(self.id, self.email, self.first_name, self.last_name,
                           self.birthday, self.creator, self.grade)
