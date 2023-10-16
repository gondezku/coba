from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name.widget = forms.TextInput(attrs={'class':'form-control px-0','placeholder':"first name"})
    last_name.widget = forms.TextInput(attrs={'class':'form-control px-0','placeholder':"last name"})
    email.widget = forms.TextInput(attrs={'class':'form-control px-0','placeholder':"e-mail"})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control px-0'
        self.fields['password1'].widget.attrs['class'] = 'form-control px-0'
        self.fields['password2'].widget.attrs['class'] = 'form-control px-0'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 're-type password'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('section',)
        widgets = {'section' : forms.Select(attrs={'class':'ml-1'})}