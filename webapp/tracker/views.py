from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tracker.models import *
from django.db.models import Min, Avg, Count

def index(request):
    return render(request, "tracker/index.html", {})
def addGrocer(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        branch_name = request.POST.get('branch_address')
        branch_image = request.FILES.get('branch_image')

        # ! we need data validation 
        # ! try catch saving database entry

        store, created = GroceryStore.objects.get_or_create(name=store_name)
        branch = Branch(address = branch_name, grocery_store = store, image = branch_image)
        
        branch.save()
        if created:
            store.save()
        return HttpResponseRedirect(reverse('allGrocer'))
    else:
        # request.method = GET
        return render(request, "tracker/Grocer-add_edit.html", {
            'edit' : False
        })
def editGrocer(request, id):
    # we need to get data of a specific 
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        branch_name = request.POST.get('branch_address')
        branch_image = request.FILES.get('branch_image')
        branch_id = request.POST.get('id')

        branch = Branch.objects.get(pk = branch_id)
        branch.address = branch_name
        branch.grocery_store.name = store_name

        if branch_image is not None:
            branch.image = branch_image

        branch.save()
        branch.grocery_store.save()

        # ! redirect to idk
        return HttpResponseRedirect(reverse('allGrocer'))

    else:
        toBeEdited = Branch.objects.get(pk = id)
        # ! check if exists (if not use try catch)

        return render(request, "tracker/Grocer-add_edit.html", {
            'branch' : toBeEdited,
            'edit' : True
        })                                                          
def grocerList(request):
    return render(request, "tracker/list_view/Grocer-list.html", {
        'grocerlist':Branch.objects.all()
    })
def groceryPurchase(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        store_branch = request.POST.get('store_branch')
        pass
    else:

        return render(request, "tracker/addPurchase.html", {})
def compareGrocers(request):
    common = []
    for i in grocerList:
        for j in grocerList:
            if grocerList[i] == grocerList[j]:
                common.append(grocerList[i])

    g1 = list(set(grocerList) - set(common))
    g2 = list(set(grocerList) - set(common))
def grocerDetail(request, id):
    branch = Branch.objects.get(pk=id)

    # number of visits
    visits = branch.purchases.count()
    costs = branch.getCosts()
    # first 10 items
    a = PurchaseItems.objects.filter(purchase__grocery_store = branch).order_by('-id')[:20]
    a = list(a)

    return render(request, "tracker/detail_view/Grocer_detail.html",{
        'branch': branch,
        'visits': visits,
        'costs': costs,
        'itemsHistory': a
    })
def productDetail(request, id):
    item = Item.objects.get(pk=id)
    allSoldHistory = PurchaseItems.objects.filter(item=item)
    data = allSoldHistory.aggregate(lowest = Min('price'),
                                    avg = Avg('price'),
                                    count = Count('id'))
    lowest = data.get('min')
    avg = data.get('avg')
    count = data.get('count')
    return render(request, "tracker/detail_view/Product_detail.html", {
        'price_avg': avg,
        'price_min': lowest,
        'item' : item,
        'timesBought': count
    })