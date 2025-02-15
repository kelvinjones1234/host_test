from django.contrib import admin
from .models import (
    ProductCategory,
    Data,
    DataSettings,
    Airtime,
    AirtimeSettings,
    Electricity,
    ElectricitySettings,
    Cable,
    CableSettings,
    Epin,
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory


#######################################################################################
####### DATA #####################################################################


def disable_data_plans(modeladmin, request, queryset):
    queryset.update(is_active=False)


disable_data_plans.short_description = "Disable selected data plans"


def enable_data_plans(modeladmin, request, queryset):
    queryset.update(is_active=True)


enable_data_plans.short_description = "Enable selected data plans"


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        "network",
        "plan_type",
        "data_plan",
        "plan_id",
        "price",
        "is_active",
    )
    actions = [disable_data_plans, enable_data_plans]
    list_filter = ("network", "plan_type", "is_active")


def network_id_one(modeladmin, request, queryset):
    queryset.update(network_id="1")


network_id_one.short_description = "Set to 1"


def network_id_two(modeladmin, request, queryset):
    queryset.update(network_id="2")


network_id_two.short_description = "Set to 2"


def network_id_three(modeladmin, request, queryset):
    queryset.update(network_id="3")


network_id_three.short_description = "Set to 3"


def network_id_four(modeladmin, request, queryset):
    queryset.update(network_id="4")


network_id_four.short_description = "Set to 4"


@admin.register(DataSettings)
class DataSettingsAdmin(admin.ModelAdmin):
    model = DataSettings
    actions = [network_id_four, network_id_three, network_id_two, network_id_one]
    list_display = ("network", "plan_type", "is_active", "network_id")
    list_filter = ("network",)


#######################################################################################
####### AIRTIME #####################################################################


@admin.register(Airtime)
class AirtimeAdmin(admin.ModelAdmin):
    model = Airtime
    list_display = (
        "airtime_type",
        "network",
        "category",
    )


def network_id_one(modeladmin, request, queryset):
    queryset.update(network_id="1")


network_id_one.short_description = "Set to 1"


def network_id_two(modeladmin, request, queryset):
    queryset.update(network_id="2")


network_id_two.short_description = "Set to 2"


def network_id_three(modeladmin, request, queryset):
    queryset.update(network_id="3")


network_id_three.short_description = "Set to 3"


def network_id_four(modeladmin, request, queryset):
    queryset.update(network_id="4")


network_id_four.short_description = "Set to 4"


@admin.register(AirtimeSettings)
class AirtimeAdmin(admin.ModelAdmin):
    model = AirtimeSettings
    actions = [network_id_four, network_id_three, network_id_two, network_id_one]
    list_filter = ("network",)
    list_editable = ("is_active",)
    list_display = ("network", "network_id", "airtime_type", "is_active")


########################################################################################
#########################CABLE#############################################


@admin.register(Cable)
class CableAdmin(admin.ModelAdmin):
    model = Cable
    list_display = (
        "cable_name",
        "cable_plan",
        "plan_id",
        "price",
        "category",
    )


@admin.register(CableSettings)
class CableSettingsAdmin(admin.ModelAdmin):
    model = CableSettings
    list_display = (
        "cable_name",
        "cable_id",
        "is_active",
    )


#############################################################################
####################ELECTRICITY BILL###########################


@admin.register(Electricity)
class ElectricityAdmin(admin.ModelAdmin):
    model = Electricity
    list_display = (
        "disco_name",
        "meter_type",
        "plan_id",
        "category",
        "is_active",
    )
    list_filter = ("meter_type", "is_active")


@admin.register(ElectricitySettings)
class ElectricitySettingsAdmin(admin.ModelAdmin):
    model = ElectricitySettings
    list_display = (
        "meter_type",
        "is_active",
    )


@admin.register(Epin)
class EpinAdmin(admin.ModelAdmin):
    model = Epin
    list_display = (
        "exam_type",
        "price",
        "category",
    )
