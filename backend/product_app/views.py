from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from setting_app.models import Terms, Policy, About
from api_app.models import ApiSettings
from .models import (
    ProductCategory,
    Data,
    DataSettings,
    AirtimeSettings,
    CableSettings,
    Cable,
    Electricity,
    ElectricitySettings,
)
from .serializers import (
    ProductCategorySerializer,
    NetworkSerializer,
    DataSerializer,
    PlanTypeSerializer,
    AirtimeTypeSerializer,
    CableCategorySerializer,
    CablePlansSerializer,
    ElectricitySerializer,
    ElectricitySettingsSerializer,
)
from setting_app.serializers import TermsSerializer, PolicySerializer, AboutSerializer
from api_app.serializers import ApiSettingsSerializer


class DataPlansView(generics.ListAPIView):
    serializer_class = DataSerializer

    def get_queryset(self):
        network_type = self.kwargs["network_type"]
        data_plan_type = self.kwargs["data_plan_type"]
        return Data.objects.filter(
            network=network_type, plan_type=data_plan_type, is_active=True
        )


class PlanTypeView(generics.ListAPIView):
    serializer_class = PlanTypeSerializer

    def get_queryset(self):
        network_type = self.kwargs["network_type"]
        return DataSettings.objects.filter(network=network_type)


class AirtimeTypeView(generics.ListAPIView):
    serializer_class = AirtimeTypeSerializer

    def get_queryset(self):
        network_type = self.kwargs["network_type"]
        return AirtimeSettings.objects.filter(network=network_type)


class CablePlansView(generics.ListAPIView):
    serializer_class = CablePlansSerializer

    def get_queryset(self):
        cable_plans = self.kwargs["cable_category"]
        return Cable.objects.filter(cable_name=cable_plans)


class ElectricityView(APIView):
    def get(self, request):
        electricity = Electricity.objects.all()
        serializer = ElectricitySerializer(electricity, many=True)
        return Response(serializer.data)


class ElectricitySettingsView(APIView):
    def get(self, request):
        settings = ElectricitySettings.objects.all()
        serializer = ElectricitySettingsSerializer(settings, many=True)
        return Response(serializer.data)


class CombinedDataView(APIView):
    def get(self, request):
        try:
            product_data = ProductCategory.objects.all()
            terms_and_conditions = Terms.objects.all()
            privacy_policy = Policy.objects.all()
            about = About.objects.all()
            api_settings = ApiSettings.objects.all()
            cable_categories = CableSettings.objects.all()

            data_networks = list(
                DataSettings.objects.values("network", "network_id").distinct()
            )
            airtime_networks = list(
                AirtimeSettings.objects.values("network", "network_id").distinct()
            )

            serialized_data = {
                "productData": ProductCategorySerializer(product_data, many=True).data,
                "terms": TermsSerializer(terms_and_conditions, many=True).data,
                "policy": PolicySerializer(privacy_policy, many=True).data,
                "about": AboutSerializer(about, many=True).data,
                "apiSettings": ApiSettingsSerializer(api_settings, many=True).data,
                "dataNetworks": data_networks,
                "airtimeNetworks": airtime_networks,
                "cableCategories": CableCategorySerializer(
                    cable_categories, many=True
                ).data,
            }

            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Data generation failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
