from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Panner'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-creams'),
)
STATE_CHOICE = (
    ('ANDHRA PRADESH', 'ANDHRA PRADESH'),
    ('ARUNACHAL PRADESH', 'ARUNACHAL PRADESH'),
    ('ASSAM', 'ASSAM'),
    ('BIHAR', 'BIHAR'),
    ('CHHATTISGARH', 'CHHATTISGARH'),
    ('GOA', 'GOA'),
    ('GUJARAT', 'GUJARAT'),
    ('HARYANA', 'HARYANA'),
    ('HIMACHAL PRADESH', 'HIMACHAL PRADESH'),
    ('JHARKHAND', 'JHARKHAND'),
    ('KARNATAKA', 'KARNATAKA'),
    ('KERALA', 'KERALA'),
    ('MADHYA PRADESH', 'MADHYA PRADESH'),
    ('MAHARASHTRA', 'MAHARASHTRA'),
    ('MANIPUR', 'MANIPUR'),
    ('MEGHALAYA', 'MEGHALAYA'),
    ('MIZORAM', 'MIZORAM'),
    ('NAGALAND', 'NAGALAND'),
    ('ODISHA', 'ODISHA'),
    ('PUNJAB', 'PUNJAB'),
    ('RAJASTHAN', 'RAJASTHAN'),
    ('SIKKIM', 'SIKKIM'),
    ('TAMIL NADU', 'TAMIL NADU'),
    ('TELANGANA', 'TELANGANA'),
    ('TRIPURA', 'TRIPURA'),
    ('UTTAR PRADESH', 'UTTAR PRADESH'),
    ('UTTARAKHAND', 'UTTARAKHAND'),
    ('WEST BENGAL', 'WEST BENGAL'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image=models.ImageField(upload_to='product')
    def __str__(self):
        return self.title

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    

STATUS_CHOICES = (
('Accepted', 'Accepted'), ('Packed', 'Packed'),
('On The Way', 'On The Way'),
('Delivered', 'Delivered'),
('Cancel', 'Cancel'), ('Pending', 'Pending'),)

class Payment(models.Model):   
       user = models.ForeignKey(User,on_delete=models.CASCADE)
       amount =models. FloatField()
       status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
       paid = models.BooleanField(default=False)

class OrderPlaced (models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       #customer = models.ForeignKey(Customer, on_delete=models. CASCADE)
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       quantity =models.PositiveIntegerField(default=1)
       ordered_date=models.DateTimeField(auto_now_add=True)
       status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
      
       
       @property
       def total_cost(self):
            return self.quantity*self.product.discounted_price
        
class Wishlist(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)