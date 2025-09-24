from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('staff/products/add/', views.ProductAddView.as_view(), name='product-add'),
    path('staff/products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('add-to-basket/', views.add_to_basket, name='add-to-basket'),
    path('basket/', views.basket_view, name='basket'),
    path('purchase-history/', views.purchase_history_view, name='purchase-history'),  
    path('history/', views.purchase_history_view, name='history'),  
    path('staff/baskets/', views.StaffBasketReviewView.as_view(), name='staff-baskets'),
    path('staff/baskets/<int:basket_id>/review/', views.review_basket, name='review-basket'),
    path('staff/customers/', views.StaffCustomerSearchView.as_view(), name='staff-customers'),
    path('staff/customers/<int:pk>/', views.StaffCustomerDetailView.as_view(), name='customer-detail'),
    path('register/', views.RegisterView, name='register'),
    path('logout/', views.Logout, name='logout'),
]