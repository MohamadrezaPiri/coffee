from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length= 255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

class Items(models.Model):
    name = models.CharField(max_length= 255)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'items'

class Hall(models.Model):
    name = models.CharField(max_length= 255)

    def __str__(self):
        return self.name

class Table(models.Model):
    name = models.CharField(max_length=255)
    is_free = models.BooleanField(default= True)
    hall = models.ForeignKey(Hall, on_delete= models.PROTECT)

    def __str__(self):
        return self.name

class Order(models.Model):

    STATUS_COMPLETE = 'COM'
    STATUS_PENDING = 'PEN'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
    ]

    table = models. ForeignKey(Table, on_delete=models.CASCADE)
    orderid = models.TextField()
    payment_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def total_price(self):
        items = OrderDetail.objects.filter(order=self)
        sum = 0
        for item in items:
            price = item.price()
            sum += price
        if len(items) > 0:
            return sum
        else:
            return 0

    def __str__(self):
        return self.orderid
    
class OrderDetail(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    item = models.ForeignKey(Items, on_delete= models.CASCADE)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name= 'detail')
    
    def price(self):
        return self.item.price * self.quantity
        

