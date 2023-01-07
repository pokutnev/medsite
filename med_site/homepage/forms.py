from django import forms
from .models import *

class AddLoginForm(forms.Form):
    login       = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"type": "log", "placeholder": "Login"}))
    password    = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"type": "password", "placeholder": "Password"}))

class AddRegistForm(forms.Form):
    login       = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"type": "log", "placeholder": "Login"}))
    password1   = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"type": "password", "placeholder": "Password"}))
    sfc         = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"type": "sfc", "placeholder": "Your SFC"}))
    address     = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"type": "address", "placeholder": "Address"}))
    phone_num   = forms.CharField(max_length=20,  widget=forms.TextInput(attrs={"type": "phone_num", "placeholder": "Phone Number"}))

class AppointmentForm(forms.Form):
    meettime    = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local", "id":"localdate", "name":"date"}))

class AppointmentForm2(forms.Form):
    customer    = forms.IntegerField()
    doctor      = forms.IntegerField()
    meettime    = forms.DateTimeField()
    diagnosis   = forms.CharField()

class AddDocProf(forms.Form):
    prof = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Enter Your Profession"}))

class DiagForm(forms.Form):
    diag = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Enter new diagnos"}))