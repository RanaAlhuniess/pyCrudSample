import django_tables2 as tables
from django.contrib.auth.models import User


class AccountTable(tables.Table):
    actions = tables.TemplateColumn(verbose_name=('Actions'),
                                    template_name='accounts/actions_column.html',
                                    orderable=False
                                    )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap.html"
        fields = ("username", "first_name", "last_name", "email",
                  "is_active", )
