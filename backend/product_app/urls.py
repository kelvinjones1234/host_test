from django.urls import path
from .views import (
    # ProductCategoryView,
    # DataNetworkView,
    DataPlansView,
    PlanTypeView,
    # AirtimeNetworkView,
    AirtimeTypeView,
    # CableCategoryView,
    CablePlansView,
    ElectricityView,
    ElectricitySettingsView,
    CombinedDataView,
)

urlpatterns = [
    # path('product-categories/', ProductCategoryView.as_view(), name='product_category'),
    # # Data backend endpoints
    # path('data-network/', DataNetworkView.as_view(), name='unique_data_networks'),
    path(
        "data/plan-type/<str:network_type>/", PlanTypeView.as_view(), name="plan_type"
    ),
    path(
        "data/plans/<str:network_type>/<int:data_plan_type>/",
        DataPlansView.as_view(),
        name="data_plan",
    ),
    # Airtime backend endpoints
    # path('airtime-network/', AirtimeNetworkView.as_view(), name='airtime_airtime_network'),
    path(
        "airtime/airtime-type/<str:network_type>/",
        AirtimeTypeView.as_view(),
        name="airtime_type",
    ),
    # Cable subscription endpoints
    # path('cable-subscription/category/', CableCategoryView.as_view(), name='cable_categories'),
    path("category/<int:cable_category>/", CablePlansView.as_view(), name="cable_plan"),
    # Electricity bill endpoints
    path("electricity-bill/", ElectricityView.as_view(), name="electricity_bill"),
    path(
        "electricity-settings/",
        ElectricitySettingsView.as_view(),
        name="electricity_bill_settings",
    ),
    path("combined-data/", CombinedDataView.as_view(), name="combined-data"),
]
