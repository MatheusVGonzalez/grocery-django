from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

def Index(request):
    num_products = Product.objects.all().count()
    num_customers = UserProfile.objects.filter(user_type='customer').count() 
    num_staff = UserProfile.objects.filter(user_type='staff').count() 
    
    recent_products = Product.objects.all().order_by('-created_date')[:5]
    
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    
    context = {
        'num_products': num_products,
        'num_customers': num_customers,
        'num_staff': num_staff,
        'recent_products': recent_products,
        'num_visits': num_visits,
    }
    
    return render(request, 'index.html', context)

class ProductView(generic.ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = self.request.user.userprofile
            except:
                pass
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.userprofile.user_type == 'staff' 
        except:
            return False

class CustomerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.userprofile.user_type == 'customer' 
        except:
            return False

class StaffProductView(LoginRequiredMixin, StaffRequiredMixin, generic.ListView):
    model = Product
    template_name = 'staff/product_management.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductAddView(LoginRequiredMixin, StaffRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'staff/product_add.html'
    success_url = reverse_lazy('products')
    
    def form_valid(self, form):
        messages.success(self.request, f"Product '{form.instance.name}' added ")
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'staff/product_update.html'
    success_url = reverse_lazy('products') 

    def form_valid(self, form):
        messages.success(self.request, f"Product '{form.instance.name}' updated")
        return super().form_valid(form)

@login_required
def add_to_basket(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'customer':  
            messages.error(request, 'Only customers can add items to basket.')
            return redirect('index')
    except:
        messages.error(request, 'Please complete your profile setup.')
        return redirect('index')
    
    current_basket, created = Basket.objects.get_or_create(
        customer=request.user,
        status='pending',
        defaults={'created_date': timezone.now()}
    )
    
    if request.method == 'POST':
        form = AddToBasketForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            basket_item, created = BasketItem.objects.get_or_create(
                basket=current_basket,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                basket_item.quantity += quantity
                basket_item.save()
                messages.success(request, f'Updated {product.name} quantity in your basket.')
            else:
                messages.success(request, f'Added {product.name} to your basket.')
            
            return redirect('basket')
    else:
        form = AddToBasketForm()
    
    return render(request, 'customer/add_to_basket.html', {'form': form})

@login_required
def basket_view(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'customer':
            messages.error(request, 'Only customers can view basket.')
            return redirect('index')
    except:
        messages.error(request, 'Please complete your profile setup.')
        return redirect('index')
    
    try:
        current_basket = Basket.objects.get(customer=request.user, status='pending')
        basket_items = current_basket.basket_items.all()
    except Basket.DoesNotExist:
        current_basket = None
        basket_items = []
    
    context = {
        'basket': current_basket,
        'basket_items': basket_items,
    }
    
    return render(request, 'customer/basket.html', context)

class StaffBasketReviewView(LoginRequiredMixin, StaffRequiredMixin, generic.ListView):
    model = Basket
    template_name = 'staff/basket_review.html'
    context_object_name = 'baskets'
    
    def get_queryset(self):
        return Basket.objects.filter(status='pending').order_by('-created_date')

@login_required
def review_basket(request, basket_id):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'staff': 
            messages.error(request, 'Only staff can review baskets.')
            return redirect('index')
    except:
        messages.error(request, 'Access denied.')
        return redirect('index')
    
    basket = get_object_or_404(Basket, id=basket_id, status='pending')
    
    if request.method == 'POST':
        form = BasketReviewForm(request.POST)
        if form.is_valid():
            basket.status = form.cleaned_data['status']
            basket.review_comments = form.cleaned_data['review_comments']
            basket.staff_reviewer = request.user
            basket.review_date = timezone.now()
            basket.save()
            
            if basket.status == 'approved':
                PurchaseHistory.objects.create(
                    customer=basket.customer,
                    basket=basket,
                    total_amount=basket.get_total_price()
                )
            
            messages.success(request, f'Basket has been {basket.get_status_display().lower()}.')
            return redirect('staff-baskets')
    else:
        form = BasketReviewForm()
    
    context = {
        'basket': basket,
        'form': form,
    }
    
    return render(request, 'staff/review_basket.html', context)

class CustomerHistoryView(LoginRequiredMixin, CustomerRequiredMixin, generic.ListView):
    model = PurchaseHistory
    template_name = 'customer/purchase_history.html'
    context_object_name = 'purchases'
    paginate_by = 10
    
    def get_queryset(self):
        return PurchaseHistory.objects.filter(customer=self.request.user)

class StaffCustomerSearchView(LoginRequiredMixin, StaffRequiredMixin, generic.ListView):
    model = User
    template_name = 'staff/customer_search.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return User.objects.filter(userprofile__user_type='customer').order_by('-date_joined')

class StaffCustomerDetailView(LoginRequiredMixin, StaffRequiredMixin, generic.DetailView):
    model = User
    template_name = 'staff/customer_detail.html'
    context_object_name = 'customer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        context['purchase_history'] = PurchaseHistory.objects.filter(customer=customer)
        context['baskets'] = Basket.objects.filter(customer=customer).order_by('-created_date')
        return context

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['uname']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=uname,
                        password=password,
                        email=email,
                        first_name=fname,
                        last_name=lname
                    )
                    
                    UserProfile.objects.create(
                        user=user,
                        user_type='customer'  
                    )
                    
                    messages.success(request, f'Account created')
                    return redirect('login')
                    
            except Exception as e:
                messages.error(request, 'Username already exists or other error')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def Logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')

@login_required
def purchase_history_view(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'customer':
            messages.error(request, 'Only customers can view')
            return redirect('index')
    except:
        messages.error(request, 'Please complete your profile')
        return redirect('index')
    
    purchases = PurchaseHistory.objects.filter(customer=request.user).order_by('-purchase_date')
    
    context = {
        'purchases': purchases,
    }
    return render(request, 'customer/purchase_history.html', context)
