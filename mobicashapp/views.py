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
def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

def news_today(request):
    date = dt.date.today()
    images= Project.objects.all()
    current_user=request.user
    myprof=Profile.objects.filter(id=current_user.id).first()
    
    if request.method == 'POST':
        form = uploadimageForm(request.POST)
        if form.is_valid():
            print('valid')
            title = form.cleaned_data['your_title']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(title = title,email =email)
            recipient.save()
            send_welcome_email(title,email)
            HttpResponseRedirect('news_today')

    else:
        form = uploadimageForm()
    return render(request, 'home.html', {"date": date,"images":images,"myprof":myprof,"letterForm":form})


@login_required(login_url='/accounts/login/')       
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})
@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = uploadimageForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect(news_today)

    else:
        form = uploadimageForm()
    return render(request, 'new_article.html', {"form": form})

@login_required(login_url='/accounts/login/')
def mine(request,username=None):
    current_user=request.user
    pic_images=Project.objects.filter(user=current_user)
    if not username:
      username=request.user.username
      projectes = Project.objects.filter(title=username)
      user_object = request.user
  
    return render(request, 'myprofile.html', locals(),{"pic_images":pic_images})

    
@login_required(login_url='/accounts/login/')
def edit(request):
    current_user=request.user
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save(commit=False)
            image.user=current_user
            image.save()
        return redirect('newsToday')
    else:
        form=ProfileForm()
    return render(request,'edit.html',{"form":form})


@login_required(login_url='/accounts/login/')
def user(request, user_id):
    user_object = get_object_or_404(User, pk=user_id)
    if request.user == user_object:
        return redirect('myaccount')
    following = user_object.profile not in request.user.profile.follows
    user_images = user_object.profile.posts.all()
   
    return render(request, 'profile.html', locals())

@login_required(login_url='/accounts/login/')
def find(request, title):
    results = Profile.find_profile(title)
    return render(request, 'searchresults.html', locals())

@login_required(login_url='/accounts/login/')
def add_comment(request, image_id):
    current_user=request.user
    image_item=Project.objects.filter(id=image_id).first()
    prof=Profile.objects.filter(user=current_user.id).first()

  
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user.profile
            comment.post_by=prof
            comment.photo = image_item
        
            comment.save()
            return redirect("newsToday")
    else:
        form=CommentForm()
    return render(request,'comment.html',{"form":form,"image_id":image_id})


def search_results(request):

    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = Profile.search(search_term)
        # message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"users": searched_users})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
def like_it(request,id):
     likes=1
     image=Project.objects.get(id=id)
     image.likes=image.likes+1
     image.save()
     return redirect("newsToday")
@login_required(login_url='/accounts/login/') 
def page(request,id):
   
    own_page=Project.objects.filter(id=id)
    all=Rates.objects.filter(project=id) 
    if request.method == 'POST':
        form = VotesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project =id
            rate.save()
        return redirect('own_page',id)
        
    else:
        form = VotesForm() 
        calcul=Rates.objects.filter(project=id)
        usability=[]
        design=[]
        content=[]
        aver_usability=0
        aver_design=0
        aver_content=0
    for i in calcul:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content)

        if len(usability)>0 or len(design)>0 or len(content)>0:
            aver_usability+=round(sum(usability)/len(usability))
            aver_design+=round(sum(design)/len(design))
            aver_content+=round(sum(content)/len(content))
        else:
            aver_usability=0.0
            aver_design=0.0
            aver_content=0.0
   

    return render(request, 'page.html', {"own_page": own_page,"all":all,"form":form,"usability":aver_usability,"design":aver_design,"content":aver_content})

def search_results(request):

    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_articles = Project.search_by_title(search_term)
        print(searched_articles)
        # message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"projectes": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})