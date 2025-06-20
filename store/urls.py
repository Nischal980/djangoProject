from django.urls import path
from . import views
from store.views import update_prices_view



urlpatterns = [
    path('',views.home, name='home'),
    path('about/', views.about, name ='about'),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('product/<int:pk>',views.product, name='product'),
    path('recommend/',views.recommended, name='recommended'),
    path('update_user/', views.update_user, name ='update_user'),
    path('update_password/', views.update_password, name ='update_password'),
    path('update_info/', views.update_info, name ='update_info'),
    path('search/', views.search, name ='search'),
    path('add_order/', views.add_order, name ='add_order'),
    path('order_details/',views.order_details, name ='order_details'),
     path('update-prices/', update_prices_view, name='update_prices'),
]

