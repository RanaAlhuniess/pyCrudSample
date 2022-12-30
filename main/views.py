from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django_tables2 import SingleTableView, LazyPaginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CustomerSerializer
from .tables import CustomerTable
from .models import Customer
from .customerService import CustomerService
from .forms import CustomerForm



class CustomerView(FormView):
    model = Customer
    customerService = CustomerService()
    template_name = 'main/customer_form.html'
    form_class = CustomerForm
    
    @method_decorator(login_required)
    def get(self, request,id=None):
        form = self.form_class
        if id:
            try:
                customer = get_object_or_404(Customer, pk=id)
                form = self.form_class(instance=customer)
            except Exception as err:
                return redirect("/home")

        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def post(self, request,id=None):
        form = self.form_class
        user = request.user
        if id:
            try:
                customer = get_object_or_404(Customer, pk=id)
                form = CustomerForm(request.POST, instance=customer)
            except Exception as err:
                return redirect("/home")
        else :
            form = CustomerForm(request.POST)
        
        if form.is_valid():
            
            if id:
                self.customerService.update(customer)
            else :
                customer = form.save(commit=False)
                self.customerService.create(customer, user.id)
            return redirect("/home")

        return render(request, self.template_name, {"form": form})


class CustomerListView(SingleTableView):
    model = Customer
    table_class = CustomerTable
    template_name = 'main/home.html'
    redirect_url = "/home"
    paginator_class = LazyPaginator
    customerService = CustomerService()

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return super().get_context_data(**kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get("customer-id")
        if customer_id:
            try:
                self.customerService.delete(customer_id)
            except Exception as err:
                return redirect(self.redirect_url)
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if (request.GET.get('sync_customer')):
            try:
                user = self.request.user
                self.customerService.sync_customer(user.id)
            except Exception as err:
                return redirect(self.redirect_url)
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)



class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customer to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nationality']