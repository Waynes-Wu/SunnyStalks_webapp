from django.contrib import admin

from .models import *
admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Item)
admin.site.register(PurchaseHistory)
admin.site.register(PurchaseItems)