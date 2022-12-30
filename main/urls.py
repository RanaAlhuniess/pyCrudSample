from django.urls import path,include
from .views import CustomerListView, CustomerView, CustomerViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', CustomerListView.as_view(), name='home'),
    path('home', CustomerListView.as_view()),
    path('create-customer', CustomerView.as_view(), name='create_customer'),
    path("customer/<int:id>/update", CustomerView.as_view(), name="updat_customer"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

]
