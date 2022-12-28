from django.shortcuts import render
from django.views.generic import View
from django_tables2 import SingleTableView, LazyPaginator
from .tables import PersonTable
from .models import Customer
from .CustomerService import CustomerService


def home(request):
    if (request.GET.get('sync_customer')):
        customerService = CustomerService()
        customerService.sync_customer()
    return render(request, 'main/home.html')


class CustomerView(View):
    model = Customer
    template_code = '<div></div>'


class CustomerListView(SingleTableView):
    model = Customer
    table_class = PersonTable
    template_name = 'main/home.html'
    paginator_class = LazyPaginator

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.all()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get("customer-id")
        #TODO use service
        if customer_id:
            customer = Customer.objects.filter(id=customer_id).first()
            if customer:
                customer.delete()
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
