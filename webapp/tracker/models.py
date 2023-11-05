from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username

class GroceryStore(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Branch(models.Model):
    address = models.CharField(max_length=255)
    grocery_store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE, related_name='branches')
    items = models.ManyToManyField('Item', related_name='seller', blank=True)

    def getCosts(self):
        return self.purchases.all().mean()
    
    def __str__(self):
        return f'{self.grocery_store.name} [{self.address}]'


class Item(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'[{self.brand}] - {self.name} ({self.weight} grams)'
class PurchaseHistory(models.Model):
    date = models.DateField(auto_now_add=True)
    travel_expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    grocery_store = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchases')

    def __str__(self):
        if self.nickname:
            return f'{self.nickname} - {self.date}'
        return f'{self.date}'

class PurchaseItems(models.Model):
    purchase = models.ForeignKey(PurchaseHistory, on_delete=models.CASCADE, related_name='itemsPurchased')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item} - {self.price}"