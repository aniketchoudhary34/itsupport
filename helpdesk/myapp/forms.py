from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import taskdetails, userprofile


# Create your forms here. login form banane ke liye
class LoginForm(forms.Form):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

#register form can be added similarly
class registerForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


#userprofileform
class userprofileform(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
   
    class Meta:
        model = userprofile
        fields = ['address','city','state']

#taskdetails form can be added similarly
class taskdetailform(forms.ModelForm):
    class Meta:
        model = taskdetails
        fields = ['title', 'description', 'due_date', 'reward', 'excel_file']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Task description'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'reward': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reward points'
            }),
            'excel_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        # Only active users
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())