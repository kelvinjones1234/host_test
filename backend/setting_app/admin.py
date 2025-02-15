from django.contrib import admin

from .models import Terms, Policy, About

admin.site.register(Terms)
admin.site.register(Policy)
admin.site.register(About)