# BookTown - Online Book Store

A modern e-commerce web application built with Django for selling books online. This project was developed as a final year project to demonstrate full-stack web development skills.

## 🚀 Features

- **User Authentication & Registration**: Secure login/signup system with user profiles
- **Product Catalog**: Browse books by categories with detailed product information
- **Shopping Cart**: Add/remove items with persistent cart functionality
- **Search Functionality**: Search books by title, author, or description
- **Order Management**: Place orders with email confirmation
- **Product Recommendations**: AI-powered book recommendations based on user preferences
- **Dynamic Pricing**: Automated price updates based on demand
- **Responsive Design**: Modern UI built with Tailwind CSS
- **Admin Panel**: Complete backend management system

## 🛠️ Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local media storage for product images
- **Email**: SMTP integration for order confirmations

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd djangoProject
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: If requirements.txt doesn't exist, install the following packages:*
```bash
pip install django
pip install pillow
pip install mathfilters
pip install pandas
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

Open your web browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
djangoProject/
├── cart/                 # Shopping cart functionality
├── ecom/                 # Main Django project settings
├── store/                # Main e-commerce app
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── templates/        # HTML templates
│   └── static/           # Static files (CSS, JS, images)
├── media/                # User-uploaded files
├── static/               # Static assets
└── manage.py             # Django management script
```

## 🔧 Configuration

### Email Settings

To enable email functionality for order confirmations, update the email settings in `ecom/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Database Configuration

The project uses SQLite by default. For production, consider switching to PostgreSQL or MySQL.

## 🎯 Key Features Explained

### User Management
- User registration and login
- Profile management with address and contact information
- Password change functionality

### Product Management
- Product catalog with categories
- Product images and descriptions
- Sale pricing functionality
- Author and publication information

### Shopping Experience
- Add products to cart
- Persistent cart across sessions
- Order placement with email confirmation
- Order history and tracking

### Advanced Features
- AI-powered product recommendations
- Dynamic pricing based on demand
- Search functionality across products
- Responsive design for mobile devices

## 👥 Contributing

This is a final year project. For any questions or suggestions, please contact the development team.

## 📝 License

This project is developed for educational purposes as a final year project.

## 🤝 Team

- **Nischal K.C** - Lead Developer
- Additional team members

---

**Note**: This is a development version. For production deployment, ensure proper security configurations, use environment variables for sensitive data, and configure a production database.
