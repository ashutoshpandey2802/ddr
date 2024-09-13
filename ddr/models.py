from django.db import models

class ClusterIncharge(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Variety(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CropType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Farmer(models.Model):
    code = models.CharField(max_length=255, unique=True)
    eligible_qty = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code

class DDR(models.Model):
    cluster_incharge = models.ForeignKey(ClusterIncharge, on_delete=models.CASCADE)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    farmer = models.ManyToManyField(Farmer, through='DDRFarmer')
    delivery_location = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class DDRFarmer(models.Model):
    ddr = models.ForeignKey(DDR, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    ddr_qty = models.DecimalField(max_digits=10, decimal_places=2)
