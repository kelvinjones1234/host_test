from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    transaction_pin = models.CharField(max_length=4)
    is_premium = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Wallet(models.Model):
    wallet_name = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.BigIntegerField(default=0)
    last_funded = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.wallet_name.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]


# from django.contrib.postgres.fields import JSONField  # If using PostgreSQL
# Or for Django 3.1+
from django.db.models import JSONField


class FundingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Funding Details for {self.user.username}"

    def get_bank_names(self):
        """Helper method to get bank names from stored account details"""
        return [account.get("bankName", "") for account in self.account_details]

    def get_account_numbers(self):
        """Helper method to get account numbers from stored account details"""
        return [account.get("accountNumber", "") for account in self.account_details]
