from django.shortcuts import render,  redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.views.generic import CreateView
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User , Group
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
)

from django_tables2 import SingleTableView, LazyPaginator
from .forms import RegisterForm, ChangeProfileForm
from .accountService import EmployeeService
from .tables import EmployeeTable
from .utils import (
    send_activation_email
)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "registration/register.html"
    redirect_authenticated_user = False

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a register page."
                )
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        # valid = super().form_valid(form)
        user.is_active = False
        # login(self.request, user)

        if form.is_valid():
            user = form.save()
            code = "sss"
            send_activation_email(request, user.email, code)
            messages.success(
                request, ('You are signed up. To activate the account, follow the link sent to the mail.'))
            # login(self.request, user)
            return redirect('/login')
        return form.is_valid()

    def get_success_url(self):
        return '/'


class ActivateView(View):
    @staticmethod
    def get(request, code):
        

        messages.success(
            request, ('You have successfully activated your account!'))

        return redirect('/login')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm
    accountService = EmployeeService()
    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        initial['username'] = user.username
        if hasattr(user, 'account'):
            initial['birthday'] = user.account.birthday
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        dob =  form.cleaned_data['birthday']
        self.accountService.update_account(user,dob )
        messages.success(
            self.request, 'Profile data has been successfully updated.')

        return redirect('/change/profile')

class ChangePasswordView(BasePasswordChangeView):
    template_name = 'accounts/profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, 'Your password was changed.')

        return redirect('/change/profile')

class UserListView(SingleTableView):
    model = User
    table_class = EmployeeTable
    template_name = 'accounts/account.html'
    paginator_class = LazyPaginator
    accountService = EmployeeService()

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user-id")
        if user_id:
            try:
                self.accountService.delete(user_id)
            except Exception as err:
                return redirect("/accounts")
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
