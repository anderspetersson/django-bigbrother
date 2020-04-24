from django.db import models

class ModuleStat(models.Model):
    modulename = models.CharField('Module', max_length=64)
    added = models.DateTimeField('Stat Date', auto_now_add=True)
    value = models.DecimalField('Value', max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('added',)
        verbose_name = "Module Stat"
        verbose_name_plural = 'Module Stat'

    def __str__(self):
        return self.modulename