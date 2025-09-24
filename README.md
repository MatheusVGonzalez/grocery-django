# Grocery Store Management System

A Django-based web application for managing a grocery store with separate interfaces for customers and staff members.

## Features

### Customer Features
- **User Registration & Authentication**: Register as a customer and login to access customer features
- **Product Browsing**: View all available products with details like price and creation date
- **Shopping Basket**: Add products to basket and manage quantities
- **Purchase History**: View past purchases and transaction history

### Staff Features
- **Product Management**: Add, edit, and view all products in the system
- **Basket Review**: Review and approve/deny customer baskets
- **Customer Management**: View customer details and purchase history
- **Administrative Controls**: Full access to manage the grocery store operations

## Technology Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django built-in authentication system
- **Python Version**: 3.13.7

## Project Structure

```
grocery_store/
├── manage.py
├── db.sqlite3
├── grocery_store/           # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                   # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions and classes
│   ├── forms.py            # Django forms
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── registration/       # Authentication templates
│   ├── customer/          # Customer interface templates
│   ├── products/          # Product-related templates
│   └── staff/             # Staff interface templates
└── templates/
    └── registration/       # Login and registration templates
```

## Models

### User Profile
- Extends Django's built-in User model
- Supports two user types: `customer` and `staff`

### Product
- Product information with auto-increment ID
- Name, price, creation and update timestamps

### Basket
- Customer shopping baskets with pending/approved/denied status
- Links to customer and staff reviewer

### Basket Item
- Individual items within a basket
- Product, quantity, and pricing information

### Purchase History
- Records of completed purchases
- Links approved baskets to purchase records

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd grocery_store
   ```

2. **Create virtual environment**
   ```bash
   python -m venv grocery_store_env
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   grocery_store_env\Scripts\activate
   
   # macOS/Linux
   source grocery_store_env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install django==5.2.6
   pip install sqlparse
   pip install asgiref
   pip install tzdata
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`

## Usage

### For Customers
1. **Register**: Create a new account at `/register/`
2. **Login**: Access your account at `/login/`
3. **Browse Products**: View all products at `/products/`
4. **Add to Basket**: Add items to your shopping basket at `/add-to-basket/`
5. **View Basket**: Check your current basket at `/basket/`
6. **Purchase History**: View past purchases at `/purchase-history/`

### For Staff
1. **Login**: Use staff credentials to login
2. **Manage Products**: 
   - View all products at `/products/`
   - Add new products at `/staff/products/add/`
   - Edit existing products at `/staff/products/<id>/update/`
3. **Review Baskets**: 
   - View pending baskets at `/staff/baskets/`
   - Review individual baskets at `/staff/baskets/<id>/review/`
4. **Customer Management**:
   - View all customers at `/staff/customers/`
   - View customer details at `/staff/customers/<id>/`

## URL Patterns

### Public URLs
- `/` - Homepage
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/products/` - Product listing
- `/products/<id>/` - Product detail

### Customer URLs
- `/add-to-basket/` - Add products to basket
- `/basket/` - View current basket
- `/purchase-history/` - Purchase history

### Staff URLs
- `/staff/products/add/` - Add new product
- `/staff/products/<id>/update/` - Update product
- `/staff/baskets/` - Review customer baskets
- `/staff/baskets/<id>/review/` - Review specific basket
- `/staff/customers/` - View all customers
- `/staff/customers/<id>/` - Customer details

## User Roles

### Customer
- Can register and login
- Can browse products
- Can add products to basket
- Can view purchase history
- Cannot access staff functions

### Staff
- Must be created manually or through admin
- Can manage products (add, edit, view)
- Can review and approve/deny customer baskets
- Can view customer information and history
- Full administrative access

## Features in Detail

### Authentication System
- Role-based access control
- Automatic customer registration
- Staff accounts require manual creation
- Login/logout functionality

### Product Management
- Auto-increment product IDs
- Product creation and editing
- Price management
- Creation and update timestamps

### Basket System
- Customers can add multiple products
- Quantity management
- Staff review and approval process
- Three status levels: pending, approved, denied

### Purchase Tracking
- Complete purchase history
- Links baskets to purchase records
- Transaction timestamps
- Customer purchase analytics

## Development Notes

- Uses Django's built-in authentication system
- Simple, clean UI with Bootstrap styling
- SQLite database for development (easily replaceable)
- Responsive design for mobile and desktop
- Role-based view access control

## Future Enhancements

- Payment integration
- Inventory management
- Product categories
- Search functionality
- Email notifications
- Reporting dashboard
- API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For questions or support, please contact the development team.