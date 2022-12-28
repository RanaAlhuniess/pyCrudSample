from django.shortcuts import render, redirect
from django.views.generic import View
from django_tables2 import SingleTableView, LazyPaginator
from .tables import PersonTable
from .models import Customer
from .CustomerService import CustomerService
from .forms import CustomerForm


def home(request):
    if (request.GET.get('sync_customer')):
        customerService = CustomerService()
        customerService.sync_customer()
    return render(request, 'main/home.html')


class CustomerView(View):
    model = Customer
    customerService = CustomerService()
    def get(self, request, *args, **kwargs):
        form = CustomerForm()
        return render(request, 'main/create_customer.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            self.customerService.create(customer)
            return redirect("/home")
        return render(request, 'main/create_customer.html', {"form": form})


class CustomerListView(SingleTableView):
    model = Customer
    table_class = PersonTable
    template_name = 'main/home.html'
    paginator_class = LazyPaginator
    customerService = CustomerService()

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get("customer-id")
        if customer_id:
            try:
                self.customerService.delete(customer_id)
            except Exception as err:
                return redirect("/home")
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        if (request.GET.get('sync_customer')):
            try:
                self.customerService.sync_customer()
            except Exception as err:
                return redirect("/home")
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
