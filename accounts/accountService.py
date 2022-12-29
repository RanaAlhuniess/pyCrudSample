from django.contrib.auth.models import User
from .models import Employee

class AccountService:
    def all():
        return User.objects.all()
    
    def update_account(self, user, dob):
        user.save()
        Employee.objects.update_or_create(account=user,
                                          defaults={'creator': user, 'birthday': dob})

                                    
