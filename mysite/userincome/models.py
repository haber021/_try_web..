from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Source'

    def __str__(self):
        return self.name

class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.source.name if self.source else "Uncategorized"