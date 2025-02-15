from django.db import models
from user_app.models import Wallet, User

class Transaction(models.Model):
    transaction_ref_no = models.CharField(max_length=50, verbose_name="Reference Number")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    status = models.CharField(max_length=10, default='')
    phone = models.CharField(max_length=11, default='')
    new_bal = models.CharField(max_length=50)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


