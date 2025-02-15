from rest_framework import serializers 
from .models import Transaction
from user_app.serializers import WalletSerializer
from .models import Wallet


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = (
            'transaction_ref_no', 
            'wallet',
            'transaction_type',
            'product',
            'price',
            'status',
            'phone',
            'new_bal',
            'date_create'
        )