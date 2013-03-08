from django.db import models

class ModuleStat(models.Model):
    modulename = models.CharField('Module', max_length=64)
    added = models.DateTimeField('Stat Date', auto_now_add=True)
    value = models.DecimalField('Value', max_digits=10, decimal_places=2)