import requests
from .repo import CustomerRepo
from .models import CustomerGrade
from django.contrib.auth.models import User
from requests.exceptions import HTTPError


class CustomerService:
    def sync_customer(self):
        data = self.fetchCustomer()
        to_store_list = []
        for item in data:
            location = item.get('location').get('country')
            email = item.get('email')
            name = item.get('name')
            first_name = name.get('first')
            last_name = name.get('last')
            dob = item.get('dob').get('date')
            nationality = item.get('nat')
            # customer = Customer()
            # customer.email = email
            # customer.first_name = first_name
            # customer.creator = user
            # customer.grade = grade_
            user = User.objects.first()

            grade_ = CustomerGrade.objects.first()
            # item = [email = email,
            #         first_name = first_name,
            #         last_name = last_name,
            #         nationality = nationality,
            #         birthday = dob,
            #         creator_id = user.id,
            #         grade_id = grade_.id
            #         ]
            # to_store_list.append(item)
            customerRepo = CustomerRepo()
            customerRepo.create(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                nationality=nationality,
                                birthday=dob,
                                creator_id=user.id,
                                grade_id=grade_.id
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
