from django.db import models
# Create your models here.


class Symbol(models.Model):
    symbol = models.CharField(primary_key=True, max_length=50)
    type = models.CharField(max_length=20)
    filename = models.CharField(max_length=20)

    def __str__(self):
        return self.symbol
