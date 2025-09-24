from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
from datetime import date
from django.db import transaction
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    def is_staff_member(self):
        return self.user_type == 'staff'
    
    def is_customer(self):
        return self.user_type == 'customer'

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])
    
    @property
    def product_id(self):
        return f"PROD-{self.id:04d}" 

class Basket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets')
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    staff_reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_baskets')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True, help_text="Staff comments on basket review")
    
    def __str__(self):
        return f"Basket #{self.id} - {self.customer.username} - {self.get_status_display()}"
    
    def get_absolute_url(self):
        return reverse("basket_detail", args=[str(self.id)])
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.basket_items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.basket_items.all())

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    class Meta:
        unique_together = ('basket', 'product')

class PurchaseHistory(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_history')
    basket = models.OneToOneField(Basket, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Purchase #{self.id} - {self.customer.username} - ${self.total_amount}"
    
    def get_absolute_url(self):
        return reverse("purchase_detail", args=[str(self.id)])
    
    class Meta:
        ordering = ['-purchase_date']
