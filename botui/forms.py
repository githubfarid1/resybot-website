from django import forms
from django.core.exceptions import ValidationError
from .models import ReservationType, Proxy, Account, BotCommand
from django.core.exceptions import NON_FIELD_ERRORS
import re

class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservationType
        fields = ['name']

class ProxyForm(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ['name', 'http', 'https']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password', 'payment_method_id']

class BotCommandForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (False, 'No'),
        (True, 'Yes'),
    )     

    datewanted = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}), required=True)
    timewanted = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}), required=True)    
    rundate = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}), required=True)
    runtime = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time', 'step':"1"}), required=True)
    runnow = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,  initial='', widget=forms.Select(), required=True)
    nonstop = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,  initial='', widget=forms.Select(), required=True)
    # account = forms.ModelChoiceField() 
    # proxy = forms.ChoiceField(required=True)
    class Meta:
        model = BotCommand
        fields = ['url',  'datewanted',  'timewanted',  'hoursba',  'seats',  'reservation',  'rundate',  'runtime',  'runnow',  'nonstop',  'duration',  'retry',  'minidle',  'maxidle',  'account',  'proxy']

    