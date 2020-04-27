from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'abc_123','class':'col-12'}),
        help_text="<ul><li>Username should be unique</li></ul>")
    
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'XXXXXXXXXXX','class':'col-12'}),
        help_text="<ol><li>Passwords are not stored in Raw form. Hence, even the admins cannot see your password</li><li>Password should not be too similar to your username</li><li><b>Password should not be entirely Numeric</b></li></ol>",
        label="Password")
    
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'col-12'}),label="Firstname")
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'col-12'}),label="Lastname")
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'col-12'}),help_text="If you forget your password, then your emailId will be used to reset it.")
    

    class Meta:
        fields=['username','first_name','last_name','email','password1']
        model=User

    
    def save(self,commit=True):
        user=super(CustomUserCreationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        user.username=self.cleaned_data['username']
        if commit:
            user.save()
        
        return user