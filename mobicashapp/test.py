from django.test import TestCase

from django.test import TestCase


from django.test import TestCase
from .models import Project,User,Profile,Comment
import datetime as dt

class ProjectTestClass(TestCase):
   
    def setUp(self):

        self.user = User(username='laetitia')
        self.user .save()
        
        
        self.image=Project(title='amezing',description='django app',image="project", pub_date="122",link="aaaaaa")
        self.image.save_image()

 
    def test_instance(self):
        self.assertTrue(isinstance(self.image,Project))

  

    def test_delete_method(self):
        
       
        Project.objects.all().delete()

   
   
class CommentTestClass(TestCase):

    def setUp(self):
     
        self.user1 = User(username='LAETITIA')
        self.user1.save()
        self.nature=Profile(2,user=self.user1,bios='Nature')
        self.nature.save_profile()

        self.james=Project(2,title='waaw',description='thisis my website',user=self.user1,image="project")
        # self.james.save_image()
      
        self.com=Comment(comment='amezing',comment_image=self.james,posted_by=self.nature,)
        self.com.save_com()

 
    def test_instance(self):

        self.assertTrue(isinstance(self.com,Comment))    
        
    def test_save_method(self):
        
        self.com.save_com()
        comm=Comment.objects.all()
        self.assertTrue(len(comm)>0) 
    def test_delete_method(self):
       
  
        Comment.objects.all().delete()
   
class ProfileTestClass(TestCase):
    
    def setUp(self):
        self.user1 = User(username='laetitia')
        self.user1.save()
        self.nature=Profile(2,user=self.user1,bios='hello wrold')
        self.nature.save_profile()

 
    def test_instance(self):
        self.assertTrue(isinstance(self.nature,Profile))

         
    def test_save_method(self):
      
      
        self.nature.save_profile()
        comm=Profile.objects.all()
        self.assertTrue(len(comm)>0) 

    def test_delete_method(self):
      
  
        Profile.objects.all().delete()