import django_tables2 as tables
from .models import Customer


class PersonTable(tables.Table):
    actions = tables.TemplateColumn(verbose_name=('Actions'),
                                    template_name='main/actions_column.html',
                                    orderable=False,
                                    )

    class Meta:
        model = Customer
        template_name = "django_tables2/bootstrap.html"
        fields = ("first_name", "last_name", "email", "birthday", "nationality",
                  "creator", "grade", "is_deleted", )
