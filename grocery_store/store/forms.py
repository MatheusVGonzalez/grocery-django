from django import forms
from .models import *
from datetime import date
from django.contrib.auth import get_user_model
from django.utils import timezone

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price'] 
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Product Name"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Price", "step": "0.01"}),
        }

class RegisterForm(forms.Form):
    uname = forms.CharField(required=True, label="Username", widget=forms.TextInput(attrs={"class": "form-control", "name": "uname", "placeholder": "Enter username"}))
    password = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={"class": "form-control", "name": "password", "placeholder": "Enter password"}))
    email = forms.CharField(required=True, label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "name": "email", "placeholder": "Enter email"}))
    fname = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={"class": "form-control", "name": "fname", "placeholder": "Enter first name"}))
    lname = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={"class": "form-control", "name": "lname", "placeholder": "Enter last name"}))

class AddToBasketForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Select Product",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Quantity",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

class BasketReviewForm(forms.Form):
    STATUS_CHOICES = [
        ('approved', 'Approve'),
        ('denied', 'Deny'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="Review Decision",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    review_comments = forms.CharField(
        required=False,
        label="Comments",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional comments..."})
    )

class CustomerSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by username..."})
    )