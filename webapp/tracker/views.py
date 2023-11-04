from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tracker.models import *

def index(request):
    return render(request, "tracker/index.html", {})
def addGrocer(request):
    if request.method == 'POST':
        store_name = request.method['store_name']
        branch_name = request.method['branch_address']
        costs = request.method['costs']

        # ! we need data validation 

        # ! try catch saving database entry
        store = GroceryStore(name = store_name)
        branch = Branch(address = branch_name, costs = costs)
        store.branch = branch

        branch.save()
        store.save()
        return HttpResponseRedirect(reverse('allGrocer'))
    else:
        return render(request, "tracker/addGrocer.html", {
            'edit' : False
        })
def editGrocer(request, id):
    # we need to get data of a specific 
    # 
    toBeEdited = GroceryStore.objects.get(pk = id)
    # ! check if exists (if not use try catch)

    # * assuming it exists for now


    return render(request, "tracker/addGrocer.html", {
        'grocer' : toBeEdited,
        'edit' : True
    })
    
def grocerList(request):
    return render(request, "tracker/grocerList.html", {
        'grocerlist':GroceryStore.objects.all()
    })
    pass
def groceryPurchase(request):
    pass
def compareGrocers(request):
    pass
