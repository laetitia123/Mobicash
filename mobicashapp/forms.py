from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=["username","email","password1","password2"]
class Post_image_Form(forms.Form):
    class Meta:
         model=Project
         exclude=('user','profile')

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
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         exclude = ('user', )


# class ProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['Name'].widget = forms.TextInput()

#     class Meta:
#         model = Profile
#         fields = ('Name', 'profile_picture', 'bio')


class CommentForm(forms.ModelForm):
  
    class Meta:
        model = Comment
        fields = ('comment',)
class VotesForm(forms.ModelForm):
  
    class Meta:
        model = Rates
        fields = ('usability','content','design')

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')


class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')
class uploadimageForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['editor', 'pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


#   ...................      Ajax...................


class uploadCustomerForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['editor', 'pub_date' ]
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'post-text', 
                'required': True, 
                'placeholder': 'Say something...'
            }),
        }