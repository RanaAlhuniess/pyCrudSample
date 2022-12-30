from django.contrib.auth.models import User, Group

from .repo import UserRepo, EmployeeRepo


class EmployeeService:
    userRepo = UserRepo()
    employeeRepo = EmployeeRepo()

    def all():
        return User.objects.all()

    def updateAccount(self, user, dob):
        user.save()
        self.employeeRepo.update_or_create(user, dob)

    def delete(self, userId):
        self.userRepo.delete(userId)

    def getById(self,id):
        return User.objects.filter(id=id).first()

    def getGroupByName(self,name):
        return Group.objects.get(name=name)

    def toggleUserGroup(self, user:User, groupName):
    
        if not user :
            pass

        group = self.getGroupByName(groupName)
        if self.hasGroup(user, groupName):
            try:
                group.user_set.remove(user)
            except:
                pass
        else:
            try:
                group.user_set.add(user)
            except:
                pass

    def hasGroup(self, user:User, groupName):
        return user.groups.filter(name = groupName).exists()
