from django.db import models
from django.contrib.auth.models import User
from .dto import CustomerDTO

class Customer(models.Model):
    class CustomerGrade(models.TextChoices):
        UNITEDSTATES = 'US','United States'
        FRANCE = 'FR','France'
        DENMARK = 'DE','Denmark'
        
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2,choices=CustomerGrade.choices, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200, null=True)
    birthday = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def to_dto(self):
        return CustomerDTO(self.id, self.email, self.first_name, self.last_name,
                           self.nationality, self.birthday, self.creator, self.grade)
    def get_choice(all_choices,search):
            for choice in all_choices:
                print(choice[0])
                if choice[0] == search:
                    return choice[1]
            return None 
    
    def getGradeKey(self, value):
        return dict((v,k) for k,v in self.CustomerGrade.choices).get(value) 

                           