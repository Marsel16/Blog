from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(min_length=3, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=3, max_length=20, widget=forms.PasswordInput)
