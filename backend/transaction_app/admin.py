from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('wallet', 'transaction_type', 'product', 'price', 'transaction_ref_no', 'status', 'date_create', 'new_bal')
    # readonly_fields = ('transaction_ref_no', 'transaction_type',)

admin.site.register(Transaction, TransactionAdmin)