import os
import django
from django.db.models import Q, Count, F
from main_app.models import Profile, Product, Order

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
# Create and run your queries within functions


def get_profiles(search_string=None):
    if search_string is not None:
        search_q = (Q(full_name__icontains=search_string) |
                    Q(email__icontains=search_string) |
                    Q(phone_number__icontains=search_string))
        profiles = Profile.objects.all().filter(search_q).order_by('full_name')

        if profiles:
            result = [
                (f"Profile: {profile.full_name}, "
                 f"email: {profile.email}, "
                 f"phone number: {profile.phone_number}, "
                 f"orders: {profile.order_profile.count()}")
                for profile in profiles]

            return '\n'.join(result)

    return ""


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles:
        return ""

    result = [f"Profile: {profile.full_name}, orders: {profile.order_profile.count()}" for profile in loyal_profiles]
    return '\n'.join(result)


def get_last_sold_products():
    latest_order = Order.objects.all().order_by('creation_date').last()

    if not latest_order:
        return ""

    products = latest_order.products.all().order_by('name')

    product_names = ', '.join([product.name for product in products])

    return f"Last sold products: {product_names}"


def get_top_products():
    top_products = Product.objects.annotate(num_products=Count('order_product')).filter(num_products__gt=0).order_by(
        '-num_products', 'name')[:5]

    if not top_products:
        return ""

    result = ["Top products:"]

    for product in top_products:
        result.append(f"{product.name}, sold {product.num_products} times")

    return '\n'.join(result)


def apply_discounts():
    orders = (Order.objects.annotate(num_products=Count('products'))
              .filter(num_products__gt=2, is_completed=False)
              .update(total_price=F('total_price') * 0.90))

    return f"Discount applied to {orders} orders."


def complete_order():
    oldest_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not oldest_order:
        return ''

    oldest_order.is_completed = True
    oldest_order.save()

    for product in oldest_order.products.all():
        product.in_stock -= 1

        if not product.in_stock:
            product.is_available = False
        product.save()

    return "Order has been completed!"
