from django.db import models

class Data(models.Model):
    idx         = models.IntegerField()
    lofter      = models.CharField(max_length=50)
    fodt        = models.IntegerField()
    aar         = models.IntegerField()
    mnd         = models.IntegerField()
    dag         = models.IntegerField()
    vekt        = models.DecimalField(decimal_places=2, max_digits=10)
    kat         = models.CharField(max_length=50)
    rykk        = models.IntegerField()
    stot        = models.IntegerField()
    sml         = models.IntegerField()
    sinclair    = models.DecimalField(decimal_places=2, max_digits=10)
    tau         = models.DecimalField(decimal_places=2, max_digits=10)
    klubb       = models.CharField(max_length=50)
    stevne      = models.CharField(max_length=50)