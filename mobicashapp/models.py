from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django .core.validators import MaxValueValidator

class Project(models.Model):
    name= models.CharField(max_length =60)
    adress= models.CharField(max_length =60)
    phone= models.CharField(max_length =60)
 
    profile = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projectes')
   

    # @classmethod
    # def search_by_title(cls,search_term):
    #     images = cls.objects.filter(title__icontains=search_term)
    #     return images


    def save_image(self):
        
        self.save()

    
    def delete_project(self):
       
        self.delete()

    
    def update_caption(self):
       
        pass

    
    @classmethod
    def days_news(cls,date):
        news = cls.objects.filter(pub_date__date = date)
        return news
  

    @classmethod
    def get_comments(self):
        images=cls.objects.all().prefetch_related("comment_set")
        return self.comments.all()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    Name = models.TextField(default="Any")
    contact= models.TextField(default="Any")
    profile_picture = models.ImageField(
        upload_to='users/', default='users/user.png')
    bios= models.TextField(default="Welcome !")

    
  
    def save_profile(self):
        self.save ()
    

    @classmethod
    def search(cls,username):
        profiles=cls.objects.filter(user__username__icontains=username)
        return profiles

class Comment(models.Model):
    comment= models.TextField()
    photo = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    posted_by=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.posted_by
    

    def get_comment(self,id):
        comments=Comment.objects.filter(image_id=id)
        return comments
class Rates (models.Model):
    design= models.PositiveIntegerField(default=0 ,validators=[MaxValueValidator(10)])
    usability= models.PositiveIntegerField(default=0 ,validators=[MaxValueValidator(10)])
    content= models.PositiveIntegerField(default=0 ,validators=[MaxValueValidator(10)])
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    posted_by=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
project=models.IntegerField(default=0) 