# In your Django views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import CompanyProfile


# def company_profile(request):
#     supplier = Supplier.objects.all() 
#     return render(request, 'reports/index.html', {'supplier': supplier})

def company_profile(request):
     company_profile = CompanyProfile.objects.first()
     return render(request, 'reports/index.html',{'company_profile': company_profile})

def save_company_profile(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Save data to the database
        company_profile = CompanyProfile(
            company_name=company_name,
            phone_number=phone_number,
            email=email,
            address=address
        )
        company_profile.save()

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'error'}, status=400)


# views.py
from django.shortcuts import render, redirect
from .models import CompanyProfile
from django.contrib import messages

def update_company_profile(request):
    company_profile = CompanyProfile.objects.first()  # Adjust based on your needs, like filtering for a specific company

    if request.method == 'POST':
        company_profile.company_name = request.POST.get('company_name')
        company_profile.phone_number = request.POST.get('phone_number')
        company_profile.email = request.POST.get('email')
        company_profile.address = request.POST.get('address')

        company_profile.save()

        messages.success(request, 'Company profile updated successfully!')
        return redirect('company_profile')  # Redirect to the page showing the company profile or any other page

    return render(request, 'your_template.html', {'company_profile': company_profile})
