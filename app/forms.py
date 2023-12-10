from django import forms
from .models import *

class DoctorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model=Doctor
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'password', 'confirm_password', 'address_line1', 'city', 'state', 'pincode']


class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=Patient
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'password', 'confirm_password', 'address_line1', 'city', 'state', 'pincode']

