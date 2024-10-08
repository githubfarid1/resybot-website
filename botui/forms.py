from django import forms
from django.core.exceptions import ValidationError
from .models import ReservationType, Proxy, Account, BotCommand, Multiproxy, BotCheck, Setting
from django.core.exceptions import NON_FIELD_ERRORS
import re
from datetime import datetime, date, time

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
    url = forms.CharField(initial='https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial')
    datewanted = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date', }), required=True, initial=date.today())
    timewanted = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}), required=True, initial="17:00")
    hoursba = forms.IntegerField(required=True, initial=0)   
    seats = forms.IntegerField(required=True, initial=2)
    duration = forms.IntegerField(required=True, initial=0)
    retry = forms.IntegerField(required=True, initial=3)
    minidle = forms.IntegerField(required=True, initial=3)
    maxidle = forms.IntegerField(required=True, initial=10)
    rundate = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}), required=True, initial=date.today())
    runtime = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time', 'step':"1"}), required=True, initial=datetime.strftime(datetime.now(), '%H:%M:%S'))
    runnow = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,  initial=False, widget=forms.Select(), required=True)
    nonstop = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,  initial=False, widget=forms.Select(), required=True)
    reservation = forms.ModelChoiceField(queryset=ReservationType.objects.all(), initial="<Not Set>")
    account = forms.ModelChoiceField(queryset=Account.objects.all(), initial="<Not Set>")
    proxy = forms.ModelChoiceField(queryset=Proxy.objects.all(), initial="<Not Set>")
    class Meta:
        model = BotCommand
        fields = ['url',  'datewanted',  'timewanted',  'hoursba',  'seats',  'reservation',  'rundate',  'runtime',  'runnow',  'nonstop',  'duration',  'retry',  'minidle',  'maxidle',  'account',  'proxy']


class MultiproxyForm(forms.ModelForm):
    class Meta:
        model = Multiproxy
        fields = ['name', 'value', 'value2']

class BotCheckForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (False, 'No'),
        (True, 'Yes'),
    )     
    url = forms.CharField(initial='https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial')
    startdate = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date', }), required=True, initial=date.today())
    enddate = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date', }), required=True, initial=date.today())
    seats = forms.IntegerField(required=True, initial=2)
    timewanted = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}), required=True, initial="17:00")
    hoursba = forms.IntegerField(required=True, initial=0)   
    nonstop = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,  initial=False, widget=forms.Select(), required=True)
    minidle = forms.DecimalField(required=True, initial=3.0)
    maxidle = forms.DecimalField(required=True, initial=10.0)
    retrysec = forms.DecimalField(required=True, initial=0.5)
    sendmessage = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,  initial=False, widget=forms.Select(), required=True)
    reservation = forms.ModelChoiceField(queryset=ReservationType.objects.all(), initial=1)
    account = forms.ModelChoiceField(queryset=Account.objects.all(), initial=1)
    multiproxy = forms.ModelChoiceField(queryset=Multiproxy.objects.all(), initial=1)
    minproxy = forms.IntegerField(required=True, initial=10)   
    maxproxy = forms.IntegerField(required=True, initial=50)   

    class Meta:
        model = BotCheck
        fields = ['url',  'startdate',  'enddate', 'timewanted',  'hoursba',  'seats',  'reservation',  'nonstop', 'retrysec',  'minidle',  'maxidle',  'account',  'multiproxy', 'sendmessage', 'mentionto', 'minproxy', 'maxproxy']


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['name', 'key', 'value']
