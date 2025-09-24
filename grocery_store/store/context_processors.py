def nav_pages(request):
    pages = [
        {"label": "Home", "url": "/"},
        {"label": "Products", "url": "/products/"},
    ]
    
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            if user_profile.is_staff_member():
                pages.extend([
                    {"label": "Review Baskets", "url": "/staff/baskets/"},
                    {"label": "Customer History", "url": "/staff/customers/"},
                ])
            else:
                pages.extend([
                    {"label": "My Basket", "url": "/basket/"},
                    {"label": "My History", "url": "/history/"},
                ])
        except:
            pass
        
        pages.extend([
            {"label": "Logout", "url": "/logout/"},
        ])
    else:
        pages.extend([
            {"label": "Login", "url": "/accounts/login/"},
            {"label": "Register", "url": "/register/"},
        ])
    
    return {"NAV_PAGES": pages}