from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class GroceryStore(models.Model):
    name = models.CharField(max_length=255)

class Branch(models.Model):
    address = models.CharField(max_length=255)
    grocery_store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE, related_name='branches')
    items = models.ManyToManyField('Item', related_name='branches')

    def getCosts(self):
        return self.purchases.all().mean()


class Item(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseHistory(models.Model):
    date = models.DateField(auto_now_add=True)
    travel_expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    grocery_store = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchases')

class PurchaseItems(models.Model):
    purchase = models.ForeignKey(PurchaseHistory, on_delete=models.CASCADE, related_name='itemsPurchased')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)