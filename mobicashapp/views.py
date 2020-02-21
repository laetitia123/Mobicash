from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
import datetime as dt
from .models import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import MerchSerializer,MerchSerializerpro
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .forms import NewsLetterForm



def news_today(request):
    date = dt.date.today()
    images= Project.objects.all()
    current_user=request.user
    myprof=Profile.objects.filter(id=current_user.id).first()
    
    if request.method == 'POST':
        form = uploadCustomerForm(request.POST)
        if form.is_valid():
            print('valid')
            name= form.cleaned_data['sku']
            adress= form.cleaned_data['pname']
            recipient =  Project(nme= name, adress=adress)
            recipient.save()
            # send_welcome_email(title,email)
            HttpResponseRedirect('news_today')

    else:
        form = uploadCustomerForm()
    return render(request, 'home.html', {"date": date,"images":images,"myprof":myprof,"letterForm":form})
#     sku = request.POST.get('your_name')
#     pname = request.POST.get('email')

#     recipient =  Project(pname=pname, sku=sku)
#     recipient.save()
#     # send_welcome_email(name, email)
#     data = {'success': 'You have been successfully added to mailing list'}
#     return JsonResponse(data)




def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('newsToday')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('login')

class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = Project.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)
class MerchListpro(APIView):
    def get(self, request, format=None):
        all_merch = Profile.objects.all()
        serializers =MerchSerializerpro(all_merch, many=True)
        return Response(serializers.data)




@login_required(login_url='/accounts/login/')
def add_customer(request):
    current_user = request.user
    if request.method == 'POST':
        form = uploadCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user= current_user
            article.profile= request.user
            article.save()
        return redirect(add_customer)

    else:
        form = uploadCustomerForm()
    return render(request, 'new_article.html', {"form": form})


@login_required(login_url='/accounts/login/')
def view_customer(request):
    customers = Project.objects.all()
    return render(request,'view-customer.html',{'customers':customers})    

@login_required(login_url='/accounts/login/')
def delete_customer(request):
    customers = Project.objects.all()
    return render(request,'delete.html',{'customers':customers}) 

def deleted(request,pk=None):
    object = Project.objects.get(id=pk)   
    object.delete()
    return render(request,'view-customer.html')

def update(request,pk=None):
    current_user = request.user
    if request.method == 'POST':
        if Project.objects.filter(id=pk).exists():
            form =uploadCustomerForm(request.POST, request.FILES,instance=Add.objects.get(id=pk))
        else:
            form = uploadCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('view_customer',pk.id)

    else:
        if Project.objects.filter(id=pk).exists():
            form = uploadCustomerForm(instance = Project.objects.get(id=pk))
        else:
            form = uploadCustomerForm()
    return render(request, 'new_article.html', {'form': form})


@login_required(login_url='/accounts/login/')
def edit_customer(request):
    customers = Project.objects.all()
    return render(request,'edit.html',{'customers':customers})
