from django.urls import path
from .views import CustomerListView, CustomerView
urlpatterns = [
    path('', CustomerListView.as_view(), name='home'),
    path('home', CustomerListView.as_view()),
    path('create-customer', CustomerView.as_view(), name='create_customer'),
    path("customer/<int:id>/update", CustomerView.as_view(), name="updat_customer"),
]
