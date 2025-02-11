from django.shortcuts import render
# from sales.models import Sale
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from sales.models import Order
from .models import NewSale
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Product  # Ensure you import your Product model


@login_required
@permission_required('sales.view_sales', raise_exception=True)
def sales_dashboard(request):
    sales = Sale.objects.all()
    total_sales = sales.count()
    total_revenue = sum(sale.amount for sale in sales)
    
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'sales/sales_dashboard.html', context)


def sales_list(request):
    sales = NewSale.objects.all()
    total_sales =  NewSale.objects.all().count()
    products = Product.objects.all() 
    products_list = Product.objects.all().count()
    total_sales =  NewSale.objects.all().count()
    
    context = {
        "sales": sales,
        "products_list": products_list,
        "total_sales": total_sales,
        }
    
    return render(request, 'sales/index.html', context)








def new_sales(request):
    products = Product.objects.all()
    return render(request, 'sales/new_sales.html', {'products': products})


def get_product_price(request):
    product_id = request.GET.get("product_id")
    product = Product.objects.filter(id=product_id).first()
    if product:
        return JsonResponse({"price": product.price})
    return JsonResponse({"price": 0})




# views.py
from django.http import JsonResponse
from django.shortcuts import render
from .models import NewSale
from django.http import JsonResponse



def create_sale(request):
    if request.method == 'POST':
        # Extract data from the request
        customer_name = request.POST.get('customer_name')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')

        # Convert values to correct data types
        try:
            price = float(price)
            quantity = int(quantity)
            discount = float(discount) if discount else 0.0
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

        # Calculate total after discount
        total_price = (price * quantity) - ((discount / 100) * (price * quantity))

        # Save sale to database
        # sale = NewSale.objects.create(
        #     customer=customer_name,
        #     product_name=product_name,
        #     price=price,
        #     quantity=quantity,
        #     discount=discount,
        #     total=total_price
        # )

        return JsonResponse({
            'status': 'success',
            'message': 'Sale has been successfully recorded.',
            'total': total_price
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import NewSale, Product

@csrf_exempt
def save_sale(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer_name = data.get("customer_name")
            product_id = data.get("product_id")
            quantity = int(data.get("quantity", 1))
            discount = float(data.get("discount", 0))

            product = Product.objects.get(id=product_id)

            sale = NewSale.objects.create(
                customer_name=customer_name,
                product=product,
                quantity=quantity,
                discount=discount
            )

            return JsonResponse({"success": True, "message": "Sale recorded successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    
    return JsonResponse({"success": False, "message": "Invalid request method!"})

from django.http import JsonResponse
from .models import NewSale, Product
from decimal import Decimal

def add_sale(request):
    if request.method == "POST":
        customer = request.POST.get("customer", "")
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity", 0))
        discount = Decimal(request.POST.get("discount", 0) or 0)
        payment_method = request.POST.get("payment_method")

        # Get product and price
        product = Product.objects.get(id=product_id)
        price = product.selling_price

        # Calculate total amount
        total_amount = (price * quantity) - discount

        # Save the sale
        sale = NewSale.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            price=price,
            discount=discount,
            total_amount=total_amount,
            payment_method=payment_method,
        )

        return JsonResponse({"message": "Sale added successfully!"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import calendar
from datetime import datetime
from django.shortcuts import render
from .models import NewSale

def sales_trends_chart(request):
    # Get all sales data
    sales = NewSale.objects.all()

    # Prepare monthly sales data
    monthly_sales = {}
    for sale in sales:
        month = sale.date.month  # Extract month
        monthly_sales[month] = monthly_sales.get(month, 0) + sale.total_amount

    # Ensure all months are included
    months = list(range(1, 13))
    sales_values = [monthly_sales.get(m, 0) for m in months]

    # Plot the sales trend graph
    plt.figure(figsize=(10, 5))
    sns.barplot(x=[calendar.month_abbr[m] for m in months], y=sales_values, color='navy')
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.title("Sales Trends Over the Year")

    # Save the graph as an image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_url = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    # Pass graph to template
    return render(request, 'sales/sales_trends.html', {"graph": f"data:image/png;base64,{graph_url}"})



from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from .models import NewSale
from datetime import datetime
from django import forms

# Form for Date Range Selection
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

def sales_report(request):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of current week
    start_of_month = today.replace(day=1)  # First day of the month

    # Fetch all sales records
    all_sales = NewSale.objects.all().order_by('-date')

    # Daily Sales
    daily_sales = NewSale.objects.filter(date__date=today)
    daily_total = daily_sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Weekly Sales
    weekly_sales = NewSale.objects.filter(date__date__gte=start_of_week)
    weekly_total = weekly_sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Monthly Sales
    monthly_sales = NewSale.objects.filter(date__date__gte=start_of_month)
    monthly_total = monthly_sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Date Range Sales
    form = DateRangeForm(request.GET)
    date_range_sales = None
    date_range_total = 0
    itemized_sales = {}

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        date_range_sales = NewSale.objects.filter(date__date__range=[start_date, end_date])
        date_range_total = date_range_sales.aggregate(total=Sum('total_amount'))['total'] or 0

        # Group sales by product and sum up quantities and total amount
        itemized_sales = date_range_sales.values('product__product_name').annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum('total_amount')
            ).order_by('-total_sales')


    context = {
        "all_sales": all_sales,
        "daily_sales": daily_sales,
        "daily_total": daily_total,
        "weekly_sales": weekly_sales,
        "weekly_total": weekly_total,
        "monthly_sales": monthly_sales,
        "monthly_total": monthly_total,
        "date_range_sales": date_range_sales,
        "date_range_total": date_range_total,
        "itemized_sales": itemized_sales,
        "form": form,
    }

    return render(request, "sales/sales_report.html", context)

#####################################################################################

from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
import datetime
from .models import Product
from django.utils.formats import number_format
from reports.models import CompanyProfile
from inventory.models import  Cargo
from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from .models import NewSale
from datetime import datetime
from django import forms


# Form for Date Range Selection
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


def sales_report_(request):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of current week
    start_of_month = today.replace(day=1)  # First day of the month

    # Fetch all sales records
    all_sales = NewSale.objects.all().order_by('-date')

    # Daily Sales
    daily_sales = NewSale.objects.filter(date__date=today)
    daily_total = daily_sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Weekly Sales
    weekly_sales = NewSale.objects.filter(date__date__gte=start_of_week)
    weekly_total = weekly_sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Monthly Sales
    monthly_sales = NewSale.objects.filter(date__date__gte=start_of_month)
    monthly_total = monthly_sales.aggregate(total=Sum('total_amount'))['total'] or 0

    # Date Range Sales
    form = DateRangeForm(request.GET)
    date_range_sales = None
    date_range_total = 0
    itemized_sales = {}

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        date_range_sales = NewSale.objects.filter(date__date__range=[start_date, end_date])
        date_range_total = date_range_sales.aggregate(total=Sum('total_amount'))['total'] or 0

        # Group sales by product and sum up quantities and total amount
        itemized_sales = date_range_sales.values('product__product_name').annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum('total_amount')
            ).order_by('-total_sales')

    products = Product.objects.all()
    company_details = CompanyProfile.objects.all()
    total_selling_price = sum(p.selling_price * p.stock_quantity for p in products)
    total_buying_price = sum(p.buying_price * p.stock_quantity for p in products)
    possible_profit = total_selling_price - total_buying_price
    total_received = sum(p.max_stock - p.stock_quantity for p in products)
    total_shipped = sum(p.max_stock - p.stock_quantity for p in products)
    net_movement = total_received - total_shipped

    # today_date = datetime.date.today().strftime("%B %d, %Y")
    
    
 
    context = {
        "company_details":company_details,
        "products": products,
        "total_received": total_received,
        "total_shipped": total_shipped,
        "net_movement": net_movement,
        "total_selling_price": total_selling_price,
        "total_buying_price": total_buying_price,
        # "today_date": today_date,
        "possible_profit": possible_profit,
        "all_sales": all_sales,
        "daily_sales": daily_sales,
        "daily_total": daily_total,
        "weekly_sales": weekly_sales,
        "weekly_total": weekly_total,
        "monthly_sales": monthly_sales,
        "monthly_total": monthly_total,
        "date_range_sales": date_range_sales,
        "date_range_total": date_range_total,
        "itemized_sales": itemized_sales,
        "form": form,
    }
    
    template = get_template("sales/sales_report.html")
    html_content = template.render(context)
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Stock_Report.pdf"'

    HTML(string=html_content).write_pdf(response)
    
    return response



import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from sales.models import NewSale
from reports.models import CompanyProfile 
 

# def sales_reports(request):
#     start_date = request.GET.get("start_date")
#     end_date = request.GET.get("end_date")

#     company_details = CompanyProfile.objects.all()


#     if start_date and end_date:
#         sales_list = NewSale.objects.filter(date__range=[start_date, end_date])
#     else:
#         sales_list = NewSale.objects.all()  

#     total_sales = sum(NewSale.total_amount for NewSale in sales_list)

#     today_date = datetime.date.today().strftime("%B %d, %Y")

#     context = {
#         "company_details": company_details,
#         "sales_list": sales_list,
#         "total_sales": total_sales,
#         "today_date": today_date,
#     }


#     template = get_template("sales/sales_report2.html")
#     html_content = template.render(context)

  
#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = 'inline; filename="sales_report.pdf"'

#     HTML(string=html_content).write_pdf(response)

#     return response



import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from sales.models import NewSale
from reports.models import CompanyProfile 
from django.urls import reverse

def sales_reports(request):
    if request.method == "GET":
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")

        # Ensure that dates are valid datetime.date objects
        if start_date_str and end_date_str:
            try:
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"status": "error", "message": "Invalid date format. Please use YYYY-MM-DD."}, status=400)
        else:
            return JsonResponse({"status": "error", "message": "Start and end dates are required."}, status=400)

        # Fetch company details and sales data
        company_details = CompanyProfile.objects.all()
        sales_list = NewSale.objects.filter(date__range=[start_date, end_date])

        # Check if no data is found in the selected date range
        if not sales_list:
            return JsonResponse({"status": "error", "message": "There is no data in the date range selected."}, status=404)

        # Calculate total sales
        total_sales = sum(NewSale.total_amount for NewSale in sales_list)

        # Prepare context data
        context = {
            "company_details": company_details,
            "sales_list": sales_list,
            "total_sales": total_sales,
            "today_date": datetime.date.today().strftime("%B %d, %Y"),
        }

        # Determine which template to use for regular or PDF report
        template_name = "sales/sales_report2.html"
        template = get_template(template_name)
        html_content = template.render(context)

        # Generate the PDF file if report_type is pdf
        if request.GET.get("report_type") == "pdf":
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="sales_report.pdf"'
            HTML(string=html_content).write_pdf(response)

            # Return response with PDF file
            return response

        # If AJAX, return the URL for the generated report
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            pdf_url = reverse("sales_reports") + f"?start_date={start_date.strftime('%Y-%m-%d')}&end_date={end_date.strftime('%Y-%m-%d')}&report_type=pdf"
            return JsonResponse({"status": "success", "pdf_url": pdf_url})

        # Return regular HTML response for non-AJAX requests
        return HttpResponse(html_content)

    # Return an error if the request is not GET
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
