from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("grocer/add",views.addGrocer, name='addGrocer'),
    path("grocer/edit/<int:id>",views.editGrocer, name='editGrocer'),
    path("grocer/all",views.grocerList, name='allGrocer'),
    path("grocer/<int:id>",views.grocerDetail, name='grocerDetail'),
    path("grocer/delete/<int:id>/", views.deleteGrocer, name='deleteGrocer'),

    path("purchase/add/<int:branch_id>",views.addPurchase, name='addPurchase'),
    path("purchase/<int:id>",views.purchaseDetail, name='purchaseDetail'),
    path("compare",views.compareGrocers, name='compare'),
    
    path("api/compare",views.compare_api, name='api_compare'),
    path("api/branch",views.branch_api, name='api_branch'),

    path("item/add",views.addProduct, name='addProduct'),
    path("item/edit/<int:id>",views.editProduct, name='editProduct'),
    path("item/all",views.itemList, name='allItems'),
    path("item/<int:id>",views.productDetail, name='productDetail'),
    path("item/delete/<int:id>", views.deleteProduct, name='deleteProduct'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)