from django.contrib import admin
from.import models

# Register your models here.
admin.site.site_header='MRT vegitables'

admin.site.register(models.Vender)
admin.site.register(models.Customer)
admin.site.register(models.Unit)

class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit']
    search_fields=['title','unit__title']
admin.site.register(models.Product,ProductAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['id','vender','product','qty','price','totalamt','purdate']
    search_fields=['product__title']
admin.site.register(models.Purchase,PurchaseAdmin)

class SaleAdmin(admin.ModelAdmin):
    list_display=['id','customer','product','qty','price','totalamt','saledate']
    search_fields=['product__title']
admin.site.register(models.Sale,SaleAdmin)


class InventryAdmin(admin.ModelAdmin):
    search_fields=['product__title','product__unit__title']
    list_display=['product','purqty','productunit','saleqty','totalbalqty','purdate','saledate']
admin.site.register(models.Inventry,InventryAdmin)