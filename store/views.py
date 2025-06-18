import pandas as pd 
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, Product, Quote, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from store.recommend_main import recommend, df
import random
from django.db.models import Q 
from django.http import JsonResponse
from store.topsellingproducts import update_top_selling_products
from django.core.mail import send_mail
from django.conf import settings

def update_prices_view(request):
    updated_products = update_top_selling_products()  # Get updated products list from the logic

    # Format increased products for the JSON response
    formatted_increased_products = [
        {"id": product['id'], "name": product['name'], "new_price": product['new_price']}
        for product in updated_products['increased_products']
    ]

    # Format decreased products for the JSON response
    formatted_decreased_products = [
        {"id": product['id'], "name": product['name'], "new_price": product['new_price']}
        for product in updated_products['decreased_products']
    ]

    return JsonResponse({
        "message": "Prices updated successfully!",
        "increased_products": formatted_increased_products,  # Include increased product details
        "decreased_products": formatted_decreased_products   # Include decreased product details
    })


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(author__icontains=searched))
        if not searched:
            messages.success(request, "That Product Does Not Exist...Please try Again.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})

def home(request):
    products = Product.objects.all().order_by('-created_at')
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    sale_items = Product.objects.filter(is_sale=True).order_by('-created_at')[:1]
    return render(request, 'home.html',{'products':products,'sale_items':sale_items,'random_quotes':random_quotes})

def about(request):
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    return render(request, 'about.html',{'random_quotes':random_quotes})

def login_user(request):
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, "Login Sucessfull, Welcome to Book Town")
            return redirect('home')
        else:
            messages.warning(request, "Invalide login details")
            return render(request, 'login.html', {'random_quotes':random_quotes})
    else:
        return render(request, 'login.html', {'random_quotes':random_quotes})
    

@login_required
# def add_order(request):
#     quotes = Quote.objects.all()
#     random_quotes = random.choice(quotes) if quotes.exists() else None
#     current_user = Profile.objects.get(user__id=request.user.id)
#     # print(type(current_user.user))
#     saved_cart = current_user.old_cart
#     if saved_cart:
#         converted_cart = json.loads(saved_cart)
#         cart = Cart(request)
#         for key, value in converted_cart.items():
#             product_to_add = Product.objects.get(id=int(key))
#             Order.objects.create(
#                 product=product_to_add,
#                 customer= current_user.user,
#                 quantity = value,
#                 address = current_user.address,
#                 phone = current_user.phone,
#                 )
#             cart.delete(key)
            
            
#         print("order Created")
#         messages.success(request, "Order created sucessfully, we will mail you the order detail in a while. Thankyou for  choosing us")
#         return render(request, 'cart_summary.html', {'random_quotes':random_quotes})
#     else:
#         messages.warning(request, "Empty Cart")
#         return redirect('home')

def add_order(request):
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    current_user = Profile.objects.get(user__id=request.user.id)
    
    saved_cart = current_user.old_cart
    if saved_cart:
        converted_cart = json.loads(saved_cart)
        cart = Cart(request)
        
        # Prepare the order details and total price
        order_details = ""
        total_price = 0
        for key, value in converted_cart.items():
            product_to_add = Product.objects.get(id=int(key))
            product_total_price = product_to_add.price * value
            total_price += product_total_price
            order_details += f"{product_to_add.name} (Quantity: {value}) - Price: NPR {product_total_price}\n"
            
            # Create the order
            Order.objects.create(
                product=product_to_add,
                customer=current_user.user,
                quantity=value,
                address=current_user.address,
                phone=current_user.phone,
            )
            
            # Remove item from the cart after the order is created
            cart.delete(key)
        
        # Compose the email content
        subject = "Your Order Details"
        message = f"""
        Dear {current_user.user.first_name},

        Your order has been successfully placed. Here are the details:

        {order_details}

        Total Price: NPR {total_price}

        To proceed with the payment, please login and complete your payment using the link below:

        Khalti Login Link: https://khalti.com/login  # Add Khalti login link here

        Once logged in, you can complete your payment.

        Thank you for shopping with us!

        ------------------------------------------------------------------------------
        """
        recipient_list = [current_user.user.email]  # User's email
        
        # Send the email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        # Success message to show to the user
        messages.success(request, "Order created successfully, we will mail you the order details in a while. Thank you for choosing us.")
        
        return render(request, 'cart_summary.html', {'random_quotes': random_quotes})
    else:
        messages.warning(request, "Empty Cart")
        return redirect('home')



def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out...Thank you"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password = password)
            login(request,user)
            messages.success(request, "Registration Sucessfull, Please Fill out some additional informations.")
            return redirect('update_info')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return redirect('register')
    else:
        quotes = Quote.objects.all()
        random_quotes = random.choice(quotes) if quotes.exists() else None
        return render(request, 'register.html',{'random_quotes':random_quotes,'form':form})
   
   # primary code 
# def product(request, pk):
#     product = get_object_or_404(Product, id=pk)

#     df_query = Product.objects.all().order_by('-created_at')
#     df = pd.DataFrame(list(df_query.values()))

#     print("DataFrame columns:", df.columns)

#     try:
#         result = recommend(df, product.name.replace(":", ""))
#     except ValueError as e:
#         print("Recommendation system error:", e)
#         result = []  
#     print("Recommended Books:", result)
#     recommended_products = []
#     for item_name in result:
#         item = Product.objects.filter(name__istartswith=item_name).first()
#         if item:
#             recommended_products.append(item)

#     quotes = Quote.objects.all()
#     random_quotes = random.choice(quotes) if quotes.exists() else None

#     return render(request, 'product.html', {
#         'product': product,
#         'random_quotes': random_quotes,
#         'recommended': recommended_products,
#     })

def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    df_query = Product.objects.all().values('name', 'author', 'publication', 'price', 'description')
    df = pd.DataFrame(list(df_query))
    
    print("DataFrame columns:", df.columns)
    recommended_books = recommend(df, product.name)

    recommended_products = Product.objects.filter(name__in=recommended_books)
    print(recommended_books)
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None

    return render(request, 'product.html', {
        'product': product,
        'random_quotes': random_quotes,
        'recommended': recommended_products,
    })



def recommended(request):
    result = recommend(df,"Harry Potter and the Prisoner of Azkaban Book 3")
    print(result)
    results = []
    for i, items in enumerate(result):
        item = Product.objects.filter(name__istartswith=items)
        if item:
            results.append(item)
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    return render(request, 'recommend.html',{'random_quotes':random_quotes, 'recommended':results})  


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

def order_details(request):
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    if request.user.is_authenticated:
        current_order = Order.objects.filter(customer=request.user)
        return render(request, 'order_details.html',{'random_quotes':random_quotes,'orders':current_order, 'username':request.user.first_name})
        
    pass