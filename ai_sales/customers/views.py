from django.shortcuts import render, get_object_or_404
from customers.models import Customer
from sales.models import Order
from django.shortcuts import render
from customers.models import Customer
from django.contrib.auth.decorators import login_required, permission_required

def customer_dashboard(request, customer_id):
    # customer = get_object_or_404(Customer, id=customer_id)
    # orders = Order.objects.filter(customer=customer)
    all_customers = Customer.objects.all()  # Fetch all customers

    context = {
        # 'customer': customer,
        # 'orders': orders,
        # 'total_spent': customer.total_spent(),
        # 'order_count': customer.order_count(),
        'all_customers': all_customers,  # Pass all customers to the template
    }
    return render(request, 'customers/index.html', context)


@login_required
@permission_required('customers.view_customer', raise_exception=True)
def customers_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customers_list.html', {'customers': customers})

