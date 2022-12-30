from rest_framework import serializers
from . import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id', 'email', 'first_name', 'last_name', 'nationality', 'birthday', 'grade']


