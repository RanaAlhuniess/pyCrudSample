from django.urls import path
from .views import RegisterView, ActivateView, ChangeProfileView
urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(redirect_authenticated_user=True),
        name="register",
    ),

]