from rest_framework import serializers
from .models import (
    ProductCategory,
    Data,
    DataSettings,
    AirtimeSettings,
    Cable,
    CableSettings,
    Electricity,
    ElectricitySettings,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


#########################################################################
################DATA SERIALIZER####################################


class NetworkSerializer(serializers.Serializer):
    network = serializers.CharField(max_length=10)
    network_id = serializers.CharField(max_length=2)


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"


class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSettings
        fields = "__all__"


#####################################################################
###########AIRTIME SERIALIZER###################################


class AirtimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirtimeSettings
        fields = "__all__"


#####################################################################
###########CABLE SUBSCRIPTION###################################


class CableCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CableSettings
        fields = "__all__"


class CablePlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cable
        fields = "__all__"


class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Electricity
        fields = "__all__"


class ElectricitySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricitySettings
        fields = "__all__"


# class Genericserializer(serializers.Serializer):
#   product_cat = ProductCategorySerializer()
#   data_network = NetworkSerializer()
#   airtime_network = AirtimeNetworkView()
#   cable_cat = CableCategoryView()
