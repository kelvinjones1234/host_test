from django.db import models


class ProductCategory(models.Model):
    category = models.CharField(max_length=100)
    image = models.FileField(upload_to="svgs", blank=True, null=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Product Category"


#######################################################################################
####### DATA #####################################################################


class DataSettings(models.Model):
    network = models.CharField(max_length=100, null=True, blank=True)
    network_id = models.PositiveIntegerField(default=1)
    plan_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_type

    class Meta:
        verbose_name_plural = "Data Settings"


class Data(models.Model):
    NETWORK_TYPE = (
        ("mtn", "MTN"),
        ("glo", "GLO"),
        ("airtel", "AIRTEL"),
        ("9mobile", "9MOBILE"),
    )

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    network = models.CharField(choices=NETWORK_TYPE, max_length=10)
    plan_type = models.ForeignKey(DataSettings, on_delete=models.CASCADE)
    plan_id = models.PositiveIntegerField(default=1)
    data_plan = models.CharField(max_length=50)
    price = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.network

    class Meta:
        verbose_name_plural = "Data"


#######################################################################################
####### AIRTIME #####################################################################


class AirtimeSettings(models.Model):
    network = models.CharField(max_length=100, null=True, blank=True)
    network_id = models.PositiveIntegerField(default=1)
    airtime_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.airtime_type

    class Meta:
        verbose_name_plural = "Airtime Settings"


class Airtime(models.Model):
    NETWORK_TYPE = (
        ("mtn", "MTN"),
        ("glo", "GLO"),
        ("airtel", "AIRTEL"),
        ("9mobile", "9MOBILE"),
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    airtime_type = models.ForeignKey(AirtimeSettings, on_delete=models.CASCADE)
    network = models.CharField(choices=NETWORK_TYPE, max_length=10)

    def __str__(self):
        return self.network

    class Meta:
        verbose_name_plural = "Airtime"


################################################################################################
###############CABLE SUBSCRIPTION####################################################################


class CableSettings(models.Model):
    cable_name = models.CharField(max_length=100, verbose_name="Cable Name")
    cable_id = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.cable_name

    class Meta:
        verbose_name_plural = "Cable Settings"


class Cable(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    cable_name = models.ForeignKey(CableSettings, on_delete=models.CASCADE)
    cable_plan = models.CharField(max_length=300)
    plan_id = models.PositiveIntegerField(default=0)
    price = models.CharField(max_length=10)

    def __str__(self):
        return self.cable_plan


################################################################################################
###############ELECTRICITY BILL####################################################################
class ElectricitySettings(models.Model):
    meter_type = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.meter_type

    class Meta:
        verbose_name_plural = "Electricity Settings"


class Electricity(models.Model):
    plan_id = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    disco_name = models.CharField(max_length=200)
    meter_type = models.ForeignKey(ElectricitySettings, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.disco_name

    class Meta:
        verbose_name_plural = "Electricity"


class Epin(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=200)
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return self.exam_type

    class Meta:
        verbose_name_plural = "E-Pin"
