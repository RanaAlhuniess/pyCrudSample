from django.shortcuts import render,  redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.views.generic import CreateView
from django.contrib import messages

from django.utils.encoding import force_bytes, force_str    
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 

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
from django.conf import settings

class GuestOnlyView(View):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

class RegisterView(GuestOnlyView,CreateView):
    model = User
    form_class = RegisterForm
    employeeService = EmployeeService()
    template_name = "registration/register.html"
    redirect_authenticated_user = False

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        user.is_active = False
    
        if form.is_valid():
            user = form.save()
            self.employeeService.create(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))  
            code = settings.OPT_CODE
            send_activation_email(request, user.email, code, uid)
            messages.success(
                request, ('You are signed up. To activate the account, follow the link sent to the mail.'))
            return redirect('/login')
        return form.is_valid()

    def get_success_url(self):
        return '/'


class ActivateView(View):
    @staticmethod
    def get(request, uidb64, code):
        print(uidb64)
        try:  
            uid = force_str(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(pk=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is None:
            print('Activation link is invalid!')
            return redirect('/login')

        if not code or code != settings.OPT_CODE:
            print('Activation link is invalid!')
            return redirect('/login')
        user.is_active = True  

        user.save()  
        messages.success(
            request, ('You have successfully activated your account!'))

        return redirect('/login')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm
    employeeService = EmployeeService()

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
        self.employeeService.updateAccount(user,dob )
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
    employeeService = EmployeeService()

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return super().get_context_data(**kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        employee_id = request.POST.get("employee-id")
        user_id = request.POST.get("user-id")
        if user_id:
            try:
                self.employeeService.delete(user_id)
            except Exception as err:
                return redirect("/accounts")
        elif employee_id:
                user = self.employeeService.getById(employee_id)
                if not user or not request.user.is_staff:
                    return redirect("/accounts")
                
                self.employeeService.toggleUserGroup(user, 'manager')

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)





