from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from .models import Category
from .models import Supplier
from sales.models import NewSale

def product_list(request):
  
    products = Product.objects.all() 
    products_list = Product.objects.all().count()
    total_sales =  NewSale.objects.all().count()
    
    context = {
        "products": products,
        "products_list": products_list,
        "total_sales": total_sales,
        }
    
  

    # for product in products:
    #     remaining_stock_percent = (product.stock_quantity / product.max_stock) * 100 if product.max_stock else 0
    
    #     product.critical_threshold = product.max_stock * 0.25
    #     product.low_stock_threshold = product.max_stock * 0.50
        

    return render(request, 'stock/index.html',context)


def add_supplier(request):
    supplier = Supplier.objects.all()
    number_supplier = Supplier.objects.all().count()
    total_sales =  NewSale.objects.all().count()
    
    context = {
        "supplier": supplier,
        "number_supplier": number_supplier,
        "total_sales": total_sales,
        
      
    }
    return render(request, 'stock/supplier.html',context)



from django.http import JsonResponse
from .models import Supplier


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Supplier

@csrf_exempt
def save_supplier(request):
    if request.method == "POST":
        name = request.POST.get("customer_name")
        contact_email = request.POST.get("contact_email")  # Correct field name
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")

        # Check if supplier with the same email exists
        if Supplier.objects.filter(contact_email=contact_email).exists():
            return JsonResponse({"status": "error", "message": "Supplier with this email already exists."})

        # Save to database
        supplier = Supplier.objects.create(
            name=name,
            contact_email=contact_email,
            phone_number=phone_number,
            address=address
        )

        return JsonResponse({"status": "success", "message": "Supplier saved successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category

@csrf_exempt
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        
        if name:  # Ensure name is provided
            Category.objects.create(name=name, description=description)
            return JsonResponse({"message": "Category added successfully!"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


def add_product(request):
    categories = Category.objects.all()
    return render(request, 'stock/add_product.html',{'categories': categories}) 

def get_categories(request):
    categories = Category.objects.all().values('id', 'name')
    return JsonResponse(list(categories), safe=False)


from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Supplier, Product

def add__product(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        product_name = request.POST.get('product_name')
        product_id = request.POST.get('product_id')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        # supplier_id = request.POST.get('supplier')

        # Ensure all required fields are provided
        # if category_id and product_name and product_id and price and stock_quantity and supplier_id:
        #     category = Category.objects.get(id=category_id)
        #     supplier = Supplier.objects.get(id=supplier_id)
        
        if category_id and product_name and product_id and price and stock_quantity:
            category = Category.objects.get(id=category_id)
            # supplier = Supplier.objects.get(id=supplier_id)
            
            # Create and save the product
            product = Product.objects.create(
                category=category,
                product_name=product_name,
                product_id=product_id,
                description=description,
                price=price,
                stock_quantity=stock_quantity,
                # supplier=supplier
            )
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'All fields are required'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


################################################################################################

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import urllib
import base64
from django.shortcuts import render
from .models import Product

def product_stock_graph(request):
    # Fetch product stock data
        products = Product.objects.all()
        df = pd.DataFrame(list(products.values("product_name", "stock_quantity")))
        plt.figure(figsize=(10, 5))
        sns.barplot(x="stock_quantity", y="product_name", data=df, palette="coolwarm")
        plt.xlabel("Stock Quantity", fontsize=10, fontweight="bold", color="darkblue")
        plt.ylabel("Product Name", fontsize=10, fontweight="bold", color="darkblue")
        plt.title("Stock Trends per Product", fontsize=16, fontweight="bold", color="#4B0082",loc="center", pad=20)
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        
        return render(request, "stock/stock_analysis.html", {"chart": image_base64})

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Product

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Product  # Adjust the import according to your actual model

def generate_product_pdf(request):
    # Create a response object to return the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_stocktaking.pdf"'

    # Create a canvas to generate the PDF
    pdf = canvas.Canvas(response, pagesize=letter)

    # Add title to the PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Product Stocktaking")

    # Set font for the product details
    pdf.setFont("Helvetica", 10)

    # Set initial y-coordinate for product list
    y_position = 730

    # Add table headers
    pdf.drawString(30, y_position, "Product ID")
    pdf.drawString(120, y_position, "Product Name")
    pdf.drawString(250, y_position, "Category")
    pdf.drawString(470, y_position, "Price")
    pdf.drawString(550, y_position, "S.Quantity")
    
    y_position -= 20  # Adjust the position after the header

    # Get all products from the database
    products = Product.objects.all()

    for product in products:
        pdf.drawString(30, y_position, product.product_id)
        pdf.drawString(120, y_position, product.product_name)
        pdf.drawString(250, y_position, product.category.name)  # Assuming Category model has a `name` field
        pdf.drawString(470, y_position, f"${product.price:.2f}")
        pdf.drawString(550, y_position, str(product.stock_quantity))

        y_position -= 20  # Adjust for the next product

        # Add page break if content exceeds the page height
        if y_position < 100:
            pdf.showPage()  # Create a new page
            pdf.setFont("Helvetica", 10)
            y_position = 750  # Reset y-position for the new page
            # Re-add headers on new page
            pdf.drawString(30, y_position, "Product ID")
            pdf.drawString(120, y_position, "Product Name")
            pdf.drawString(250, y_position, "Category")
            pdf.drawString(470, y_position, "Price")
            pdf.drawString(550, y_position, "Stock Quantity")
            y_position -= 20

    # Save the PDF to the response
    pdf.save()

    return response


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cargo
from .forms import CargoForm  # You'll need to create a form for this model

# View all cargo records
def view_cargo(request):
    cargos = Cargo.objects.all()
    purchased_items = Cargo.objects.all().count()
    supplier = Supplier.objects.all().count()
    number_supplier = Supplier.objects.all().count()
    total_sales =  NewSale.objects.all().count()
    
    context = {
        'cargos': cargos,
        'purchased_items':purchased_items,
        "supplier": supplier,
        "number_supplier": number_supplier,
        "total_sales": total_sales,
        
      
    }
    return render(request, 'stock/view_cargo.html', context)


# Add new cargo
def add_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_cargo')  # Redirect to view cargo after saving
    else:
        form = CargoForm()
    return render(request, 'stock/add_cargo.html', {'form': form})

# Update cargo details
def update_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('view_cargo')  # Redirect after updating
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'stock/update_cargo.html', {'form': form, 'cargo': cargo})

# Delete cargo item
def delete_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    if request.method == 'POST':
        cargo.delete()
        return redirect('view_cargo')  # Redirect after deleting
    return render(request, 'stock/delete_cargo.html', {'cargo': cargo})

############################################################ REPORTS #####################################

from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
import datetime
from .models import Product
from django.utils.formats import number_format
from reports.models import CompanyProfile
from inventory.models import  Cargo


def generate_pdf_report(request):
    cago_list =  Cargo.objects.all()
    company_details = CompanyProfile.objects.all()
    
        # Calculate total selling and buying price


    today_date = datetime.date.today().strftime("%B %d, %Y")
    
    context = {
        "company_details":company_details,
        "cago_list":cago_list,
         "today_date": today_date,

    }
    
    template = get_template("stock/cargo_report.html")
    html_content = template.render(context)
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="cargo_report.pdf"'

    HTML(string=html_content).write_pdf(response)
    
    return response


#################################################################################################


def generate_pdf(request):
    products = Product.objects.all()
    company_details = CompanyProfile.objects.all()
    
        # Calculate total selling and buying price
    total_selling_price = sum(p.selling_price * p.stock_quantity for p in products)
    total_buying_price = sum(p.buying_price * p.stock_quantity for p in products)
    possible_profit = total_selling_price - total_buying_price
    total_received = sum(p.max_stock - p.stock_quantity for p in products)
    total_shipped = sum(p.max_stock - p.stock_quantity for p in products)
    net_movement = total_received - total_shipped

    today_date = datetime.date.today().strftime("%B %d, %Y")
    
 
    context = {
        "company_details":company_details,
        "products": products,
        "total_received": total_received,
        "total_shipped": total_shipped,
        "net_movement": net_movement,
        "total_selling_price": total_selling_price,
        "total_buying_price": total_buying_price,
        "today_date": today_date,
        "possible_profit": number_format(possible_profit, decimal_pos=2)
    }
    
    template = get_template("stock/stock_report.html")
    html_content = template.render(context)
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Stock_Report.pdf"'

    HTML(string=html_content).write_pdf(response)
    
    return response



