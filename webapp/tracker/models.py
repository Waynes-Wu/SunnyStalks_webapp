from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Min, Avg, Count

class User(AbstractUser):
    def __str__(self):
        return self.username

class GroceryStore(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='grocery_store_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    address = models.CharField(max_length=255)
    grocery_store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE, related_name='branches')
    items = models.ManyToManyField('Item', related_name='seller', blank=True)
    image = models.ImageField(upload_to='branch_images/', blank=True, null=True)
    
    def getCosts(self):
        average_expense = self.purchases.aggregate(avg_expense=Avg('travel_expense'))['avg_expense']
        return average_expense if average_expense is not None else "---"
    
    def __str__(self):
        return f'{self.grocery_store.name} [{self.address}]'


class Item(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return f'[{self.brand}] - {self.name} ({self.weight} grams)'
    
    def getData(self):
        all_sold_history = PurchaseItems.objects.filter(item=self)
        data = all_sold_history.aggregate(lowest=Min('price'), 
                                        avg=Avg('price'), 
                                        count=Count('id'))
        lowest_price = data.get('lowest')
        avg_price = data.get('avg')
        times_bought = data.get('count')
        return {'lowest_price': lowest_price, 'avg_price': avg_price, 'times_bought': times_bought}
    def getLatestPrice(self, branch):
        """latest price from branch"""
        return PurchaseItems.objects.filter(item = self, purchase__grocery_store = branch).last().price  
    
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