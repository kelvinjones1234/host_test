from django.db import models

from tinymce.models import HTMLField

class Terms(models.Model):
    terms_and_conditions = HTMLField()

    def __str__(self):
        return f'Terms and conditions'
    
class Policy(models.Model):
    privacy_policy = HTMLField()

    def __str__(self):
        return f'Privacy policy'
    
class About(models.Model):
    about = HTMLField()

    def __str__(self):
        return f'About'