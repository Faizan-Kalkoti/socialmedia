from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import UserProfileInfo

class UserSignUpForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Your Username'
        self.fields['email'].label = 'Your Email'
        self.fields['password1'].label = 'Enter your password'
        self.fields['password2'].label = 'Confirm your password'

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model= UserProfileInfo
        fields =('profile_pic', 'user_description')

