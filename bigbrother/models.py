from django.db import models

class ModuleStat(models.Model):
    modulename = models.CharField(max_length=64)
    added = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)