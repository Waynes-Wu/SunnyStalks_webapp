import json
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
        return render(request, "tracker/add_edit/Grocer-add_edit.html", {
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

        return HttpResponseRedirect(reverse('allGrocer'))

    else:
        toBeEdited = Branch.objects.get(pk = id)
        # ! check if exists (if not use try catch)

        return render(request, "tracker/add_edit/Grocer-add_edit.html", {
            'branch' : toBeEdited,
            'edit' : True
        })                                                          
def grocerList(request):
    branch = Branch.objects.all()


    return render(request, "tracker/list_view/Grocer-list.html", {
        'grocerlist': branch
    })
def grocerDetail(request, id):
    branch = Branch.objects.get(pk=id)

    # number of visits
    visits = branch.purchases.count()
    costs = branch.getCosts()
    # first 20 items
    a = PurchaseItems.objects.filter(purchase__grocery_store = branch).order_by('-id')[:20]
    a = list(a)

    return render(request, "tracker/detail_view/Grocer_detail.html",{
        'branch': branch,
        'visits': visits,
        'costs': costs,
        'itemsHistory': a
    })


def addPurchase(request, branch_id):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        item_data = data.get('itemList')  
        print(item_data)
        branch = Branch.objects.get(pk = branch_id)
    
        # ! check datatype
        exp = data.get('travelExp')

        purHist = PurchaseHistory(
            travel_expense = exp if exp != -1 else None,
            grocery_store = branch
        )
        purHist.save()
        
        for item in item_data:
            itemid = item.get('id')
            new_item = ''
            if  itemid == 0:
                new_item = Item(name = item.get('itemName'),
                                brand = item.get('brand'),
                                weight = item.get('weight'))
                new_item.save()
            else:
                new_item = Item.objects.get(pk = item.get('id'))
                
            purchase_item = PurchaseItems(  purchase = purHist,
                                            item = new_item,
                                            price = item.get('price'))
            purchase_item.save()
        return HttpResponseRedirect(reverse('purchaseDetail', args = [purHist.id]))        

    else:
        branch = Branch.objects.get(pk = branch_id)
        allItems = Item.objects.all()
        
        return render(request, "tracker/addPurchase.html", {
            'items': allItems,
            'branch' : branch
        })
    
def purchaseDetail(request, id):
    purchaseHistory = PurchaseHistory.objects.get(pk = id)
    return render(request, "tracker/temp.html", {
        'purchase': purchaseHistory
    })


def compareGrocers(request):
    branchA = Branch.objects.get(pk = 2)
    branchB = Branch.objects.get(pk = 6)

    # queryset of unique item_id
    items_branchA = set(PurchaseItems.objects.filter(purchase__grocery_store=branchA).values_list('item', flat=True))
    items_branchB = set(PurchaseItems.objects.filter(purchase__grocery_store=branchB).values_list('item', flat=True))

    # set of categorized item_id
    common = items_branchA.intersection(items_branchB)
    diffA = items_branchA.difference(items_branchB)
    diffB = items_branchB.difference(items_branchA)

    common_with_prices = []
    for item in common:
        it = Item.objects.get(pk = item)
        price_A = it.getLatestPrice(branchA)
        price_B = it.getLatestPrice(branchB)
        common_with_prices.append({
            'item' : it,
            'price_A' : price_A,
            'price_B': price_B
        })

    diffA_with_prices = []
    for item in diffA:
        it = Item.objects.get(pk = item)
        price_A = it.getLatestPrice(branchA)
        diffA_with_prices.append({
            'item' : it,
            'price' : price_A,
        })
    diffB_with_prices = []
    for item in diffB:
        it = Item.objects.get(pk = item)
        price_B = it.getLatestPrice(branchB)
        diffB_with_prices.append({
            'item' : it,
            'price' : price_B,
        })

    # brand
    # item name
    # price
    # weight
    return render(request, "tracker/compare.html", {
        'branchA' : branchA,
        'branchB' : branchB,
        'common': common_with_prices,
        'diffA': diffA_with_prices,
        'diffB': diffB_with_prices
    })

def addProduct(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_brand = request.POST.get('item_brand')
        item_weight = request.POST.get('item_weight')
        item_image = request.FILES.get('item_image')

        newItem, created = Item.objects.get_or_create(
                                                    name=item_name, 
                                                    brand=item_brand, 
                                                    weight=item_weight, 
                                                    )
        if created:
            newItem.image = item_image
            newItem.save()
        else:
            raise NotImplemented
        
        return HttpResponseRedirect(reverse('allItems'))
    else:
        return render(request, "tracker/add_edit/Product-add_edit.html", {
            'edit' : False
            })

def editProduct(request, id):
    if request.method == 'POST':

        item_name = request.POST.get('item_name')
        item_brand = request.POST.get('item_brand')
        item_weight = request.POST.get('item_weight')
        item_image = request.FILES.get('item_image')
        item_id = request.POST.get('id')

        item = Item.objects.get(pk = item_id)
        # * required fields 
        item.name = item_name
        item.brand = item_brand
        item.weight = item_weight

        # * optional fields
        if item_image is not None:
            item.image = item_image
        item.save()

        return HttpResponseRedirect(reverse('allItems'))
    else:
        toBeEdited = Item.objects.get(pk = id)

        return render(request, "tracker/add_edit/Product-add_edit.html", {
            'item' : toBeEdited,
            'edit' : True
        })   
    
def itemList(request):
    item = Item.objects.all()
    items = []
    for it in item:
        data = it.getData()
        item_data = {
            'item' : it,
            'price_avg': data.get('avg_price'),
            'price_min': data.get('lowest_price'),
            'timesBought': data.get('times_bought')
        }
        items.append(item_data)

        
    return render(request, "tracker/list_view/Product-list.html", {
        'itemlist': items
        })

def productDetail(request, id):
    item = Item.objects.get(pk=id)
    allSoldHistory = PurchaseItems.objects.filter(item=item)
    # data = allSoldHistory.aggregate(lowest = Min('price'),
    #                                 avg = Avg('price'),
    #                                 count = Count('id'))
    data = item.getData()
    return render(request, "tracker/detail_view/Product_detail.html", {
        'item' : item,
        'price_avg': data.get('avg_price'),
        'price_min': data.get('lowest_price'),
        'timesBought': data.get('times_bought')
    })

