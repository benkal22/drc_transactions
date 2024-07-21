import django_tables2 as tables
from .models import Transaction

class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        template_name = 'django_tables2/tailwind.html'
        fields = ('id', 'producer', 'product', 'type', 'price', 'quantity', 'date', 'total_price')
        attrs = {"class": "min-w-full divide-y divide-gray-200"}

    total_price = tables.Column(accessor='total_price', verbose_name='Total Price')
    actions = tables.TemplateColumn(template_name='transactions/transaction_actions_column.html', orderable=False)
