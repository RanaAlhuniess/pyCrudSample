from django.contrib.auth.models import User

from .repo import UserRepo, EmployeeRepo
class EmployeeService:
    userRepo = UserRepo()
    employeeRepo = EmployeeRepo()

    def all():
        return User.objects.all()
    
    def update_account(self, user, dob):
        user.save()
        self.employeeRepo.update_or_create(user, dob)

    def delete(self, userId):
        self.userRepo.delete(userId)                               
