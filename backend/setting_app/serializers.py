from .models import Terms, Policy, About
from rest_framework import serializers

class TermsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Terms
    fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
  class Meta:
    model = Policy
    fields = '__all__'

class AboutSerializer(serializers.ModelSerializer):
  class Meta:
    model = About
    fields = '__all__'
