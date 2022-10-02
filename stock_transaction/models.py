from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StockUser(models.Model):

    user=models.OneToOneField( User, on_delete=models.CASCADE)
    account_balance= models.FloatField(default=0)
    earnt = models.FloatField(default=0)
    spent = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockPortfolio(models.Model):
    #Stock Table to maintain the stock bought
    user = models.ForeignKey(StockUser, on_delete=models.CASCADE)
    stock = models.CharField(max_length=5)
    shares = models.PositiveIntegerField(default=0)


    class Meta:
    #The ForeignKey i.e. user and a stock symbol must be unique
        unique_together = ('user', 'stock')
