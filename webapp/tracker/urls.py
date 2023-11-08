from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("grocer/add",views.addGrocer, name='addGrocer'),
    path("edit/<int:id>",views.editGrocer, name='editGrocer'),
    path("grocer/all",views.grocerList, name='allGrocer'),
    path("purchase/add",views.groceryPurchase, name='addPurchase'),
    path("compare",views.compareGrocers, name='compare'),
]