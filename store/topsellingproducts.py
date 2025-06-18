#Dynamic Pricing Algorithm

from django.db.models import Sum, F
from store.models import Order, Product
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q
from decimal import Decimal

# Define price limits
MAX_PRICE_INCREASE = Decimal('1.5')  # Max price increase multiplier (e.g., no price can increase by more than 50%)
MIN_PRICE = Decimal('5')  # Minimum price allowed

def update_top_selling_products():
    """
    Increases or decreases the price of top-selling and lowest-selling products 
    based on sales in the last 30 days. 
    - Increases price for top sellers.
    - Decreases price for low sellers.
    Returns the updated products and their new prices.
    """
    # Calculate date range for the last 30 days
    start_date = now() - timedelta(days=30)
    end_date = now()

    # Get sales data for the last 30 days
    sales_data = (
        Order.objects.filter(date__range=(start_date, end_date))
        .values('product_id')
        .annotate(total_quantity=Sum('quantity'))
    )

    # Get top 5 selling products
    top_selling_products = sorted(sales_data, key=lambda x: x['total_quantity'], reverse=True)[:5]
    lowest_selling_products = sorted(sales_data, key=lambda x: x['total_quantity'])[:5]

    # Get product IDs
    top_product_ids = [item['product_id'] for item in top_selling_products]
    lowest_product_ids = [item['product_id'] for item in lowest_selling_products]

    # Update prices for top-selling products
    updated_top_products = Product.objects.filter(id__in=top_product_ids)
    increased_products = []
    for product in updated_top_products:
        # Increase the price by 10%, but don't allow it to exceed MAX_PRICE_INCREASE
        new_price = product.price * Decimal('1.1')  # Ensure decimal multiplication
        if new_price > product.price * MAX_PRICE_INCREASE:
            new_price = product.price * MAX_PRICE_INCREASE
        product.price = new_price
        product.save()
        increased_products.append({'id': product.id, 'name': product.name, 'new_price': product.price})

    # Update prices for lowest-selling products
    updated_lowest_products = Product.objects.filter(id__in=lowest_product_ids)
    decreased_products = []
    for product in updated_lowest_products:
        # Decrease the price by 10%, but don't allow it to fall below the minimum price
        new_price = product.price * Decimal('0.9')  # Ensure decimal multiplication
        if new_price < MIN_PRICE:
            new_price = MIN_PRICE
        product.price = new_price
        product.save()
        decreased_products.append({'id': product.id, 'name': product.name, 'new_price': product.price})

    # Prepare and return separate lists for increased and decreased products
    response = {
        "message": "Prices updated successfully!",
        "increased_products": increased_products,
        "decreased_products": decreased_products
    }

    return response