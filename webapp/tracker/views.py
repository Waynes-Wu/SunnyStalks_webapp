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
        store = GroceryStore(name = 'name')
        branch = Branch(address = 'name', grocery_store = store)

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
def grocerDetails(request):
    pass
def groceryPurchase(request):
    return render(request, "tracker/addPurchase.html", {})
def compareGrocers(request):
    common = []
    for i in grocerList:
        for j in grocerList:
            if grocerList[i] == grocerList[j]:
                common.append(grocerList[i])

    g1 = list(set(grocerList) - set(common))
    g2 = list(set(grocerList) - set(common))
