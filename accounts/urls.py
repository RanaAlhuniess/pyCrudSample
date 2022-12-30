from django.urls import path
from .views import RegisterView, ActivateView, ChangeProfileView, UserListView, ChangePasswordView
urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(redirect_authenticated_user=True),
        name="register",
    ),
   
    path('activate/<uidb64>/<code>/', ActivateView.as_view(), name='activate'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),

    path('accounts', UserListView.as_view()),
]