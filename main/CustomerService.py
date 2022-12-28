import requests
from .repo import CustomerRepo
from django.contrib.auth.models import User
from requests.exceptions import HTTPError


class CustomerService:
    def sync_customer(self):
        data = self.fetchCustomer()
        for item in data:
            country = item.get('location').get('country')
            email = item.get('email')
            name = item.get('name')
            first_name = name.get('first')
            last_name = name.get('last')
            dob = item.get('dob').get('date')
            nationality = item.get('nat')
            user = User.objects.first()
            customerRepo = CustomerRepo()
            customerRepo.create(country,email=email,
                                first_name=first_name,
                                last_name=last_name,
                                nationality=nationality,
                                birthday=dob,
                                creator_id=user.id
                                )

    def fetchCustomer(self):
        try:
            # TODO: add url to setting
            response = requests.get(
                'https://randomuser.me/api/?nat=us,dk,fr&seed=abc&inc=email,name,nat,location,dob')
            response.raise_for_status()
            jsonResponse = response.json()
            return jsonResponse.get('results')
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None

    def create(self, customer):
        customerRepo = CustomerRepo()
        customerRepo.create(email=customer.email,
                            first_name=customer.first_name,
                            last_name=customer.last_name,
                            nationality=customer.nationality,
                            birthday=customer.birthday,
                            creator_id=1,
                            grade=customer.grade
                            )

    def delete(self, customerId):
        customerRepo = CustomerRepo()
        customerRepo.delete(customerId)