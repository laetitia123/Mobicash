from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget = forms.TextInput()

    class Meta:
        model = Profile
        fields = ('Name', 'profile_picture', 'bios')
        # exclude=['user']




class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')



#   ...................      Ajax...................


class uploadCustomerForm(forms.ModelForm):
    class Meta:
        model = Project
    
        exclude = ['user','profile']
        

       