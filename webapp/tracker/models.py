from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Min, Avg, Count, Sum
from django.utils.functional import cached_property

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
    def getTotalSpending(self):
        result = self.purchases.aggregate(total_spent = Sum('itemsPurchased__price'))['total_spent']
        if result is None:
            result = 0
        return result
    def getTotalTravelCost(self):
        result = self.purchases.aggregate(total_travel=Sum('travel_expense'))['total_travel']    
        if result is None:
            result = 0
        return 
    def getEfficiency(self):
        # efficiency ratio
        travelExpense = self.getTotalTravelCost()
        if travelExpense is None or travelExpense<=0:
            travelExpense = 1
        return float(self.getTotalSpending()/travelExpense)
    
    def get_efficiency_range():
        branches = Branch.objects.all()
        efficiencies = [branch.getEfficiency() for branch in branches]
        if not efficiencies:
            return None, None
        min_efficiency = float(min(efficiencies))
        max_efficiency = float(max(efficiencies))
        return (min_efficiency, max_efficiency)
    
    def getNormalizedEfficiency(self):
        min_efficiency, max_efficiency = Branch.get_efficiency_range()
        if min_efficiency is None or max_efficiency is None:
            return None        
        efficiency = self.getEfficiency()
        normalized_efficiency = (efficiency - min_efficiency) / (max_efficiency - min_efficiency)
        return int(normalized_efficiency*100)
    
    def getAvgTravelExp(self):
        average_expense = self.purchases.aggregate(avg_expense=Avg('travel_expense'))['avg_expense']
        return average_expense if average_expense is not None else "---"
    
    def popularity(self):
        count = [branch.purchases.count() for branch in Branch.objects.all()]
        maxx = max(count)
        minn = min(count)
        rating = (self.purchases.count() - minn) / (maxx - minn)
        rating = rating/0.2
        return int(rating)
    
    def __str__(self):
        return f'{self.grocery_store.name} [{self.address}]'


class Item(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

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