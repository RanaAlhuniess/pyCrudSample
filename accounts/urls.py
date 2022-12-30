from django.urls import path
from . import views

urlpatterns = [
    path(
        "register/",
        views.RegisterView.as_view(redirect_authenticated_user=True),
        name="register",
    ),
   
    path('activate/<uidb64>/<code>/', views.ActivateView.as_view(), name='activate'),

    path('change/profile/', views.ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),

    path('restore/password/', views.RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', views.RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', views.RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('accounts', views.UserListView.as_view()),
]