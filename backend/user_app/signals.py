from .models import User, Wallet
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
  if created:
    Wallet.objects.create(wallet_name=instance)
