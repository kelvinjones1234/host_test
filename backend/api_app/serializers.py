from rest_framework import serializers

from .models import ApiSettings

class ApiSettingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = ApiSettings
    fields = '__all__'