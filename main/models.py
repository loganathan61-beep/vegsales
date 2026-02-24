from django.db import models

# Create your models here.
#vender
class Vender(models.Model):
    fullname=models.CharField(max_length=50)
    adress=models.TextField()
    mobile=models.CharField(max_length=15)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.fullname
    class Meta:
        verbose_name_plural='1. Vender'
    
    #unit
class Unit(models.Model):
    title=models.CharField(max_length=50)
    shortname=models.CharField(max_length=50)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='2. Unit'
    


    #product
class Product(models.Model):
    title=models.CharField(max_length=50)
    detail=models.TextField()
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='3. Product'
    
    #purchase
class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    vender=models.ForeignKey(Vender,on_delete=models.CASCADE)
    qty=models.FloatField()
    price=models.FloatField()
    totalamt=models.FloatField(editable=False,default=0)
    purdate=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='4. Purchase'

    def save(self,*args,**kwargs):
        self.totalamt=self.qty*self.price
        super(Purchase,self).save(*args,**kwargs)

        #inventry effect
        inventry=Inventry.objects.filter(product=self.product).order_by('-id').first()
        if inventry:
            totalbal=inventry.totalbalqty+self.qty
        else:
            totalbal=self.qty

        Inventry.objects.create(
            product=self.product,
            purchase=self,
            sale=None,
            purqty=self.qty,
            saleqty=None,
            totalbalqty=totalbal
        )    


          #customer
class Customer(models.Model):
    customername=models.CharField(max_length=50,blank=True)
    customermobile=models.CharField(max_length=50)
    customeradress=models.TextField()
    def __str__(self):
        return self.customername
    class Meta:
        verbose_name_plural='7. Customer'


          #sale
class Sale(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    qty=models.FloatField()
    price=models.FloatField()
    totalamt=models.FloatField(editable=False,default=0)
    saledate=models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural='5. Sale'


    def save(self,*args,**kwargs):
        self.totalamt=self.qty*self.price
        super(Sale,self).save(*args,**kwargs)

        #inventry effect
        inventry=Inventry.objects.filter(product=self.product).order_by('-id').first()
        if inventry:
            totalbal=inventry.totalbalqty-self.qty
        
            Inventry.objects.create(
            product=self.product,
            purchase=None,
            sale=self,
            purqty=None,
            saleqty=self.qty,
            totalbalqty=totalbal
        )    


        #inventry
class Inventry(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    purchase=models.ForeignKey(Purchase,on_delete=models.CASCADE,default=0,null=True)
    sale=models.ForeignKey(Sale,on_delete=models.CASCADE,default=0,null=True)
    purqty=models.FloatField(default=0,null=True)
    saleqty=models.FloatField(default=0,null=True)
    totalbalqty=models.FloatField()
    
    
    class Meta:
        verbose_name_plural='6. Inventry'

    def productunit(self):
            return self.product.unit.title


    def purdate(self):
        if self.purchase:
            return self.purchase.purdate
        
    def saledate(self):
        if self.sale:
            return self.sale.saledate
    