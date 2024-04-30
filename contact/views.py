from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def contact(request):
    if request.method == "POST":
        data = request.POST
        fullName = data.get('full_name')
        email = data.get('email')
        message = data.get('message')
        # print(fullName)
        # print(email)
        # print(message)

        # img= request.FILES.get('img') #if you have a img
        ContactMessage.objects.create(
            full_name=fullName,
            email=email,
            message=message,
        )
        return redirect('/contact/')

        

    return render(request,"contact.html")