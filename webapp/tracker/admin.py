from django.contrib import admin

from .models import *
admin.site.register(User)
class BranchAdmin(admin.ModelAdmin):
    # Display related items in a filter_horizontal widget for easy selection.
    filter_horizontal = ('items',)

admin.site.register(Branch, BranchAdmin)
admin.site.register(GroceryStore)
admin.site.register(Item)
admin.site.register(PurchaseHistory)
admin.site.register(PurchaseItems)