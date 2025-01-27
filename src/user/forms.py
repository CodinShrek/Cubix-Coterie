from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Account
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
        username = forms.CharField(max_length=50, min_length=3)
        email = forms.EmailField(max_length=254)
        firstname = forms.CharField(max_length=100)
        lastname = forms.CharField(max_length=100)
        grade = forms.IntegerField()
        
        class Meta:
            model = Account
            fields = ("username", "email", "firstname", "lastname", "grade", "password1", "password2")
            

class UserAuthentication(forms.ModelForm):
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    
    class Meta:
        # Specify the model that this form will be based on #
        model = Account
        # Specify the fields to be used in the form #
        fields = ('username', 'password')
    
    # Clean method to validate the username and password #    
    def clean(self):
        # Retrieve the cleaned username and password data from the form #
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        # Attempt to authenticate the user using the provided credentials #
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Incorrect Login, Re-Check Credentials & Try Again")