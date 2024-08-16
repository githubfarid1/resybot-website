from django import forms
from django.core.exceptions import ValidationError
from .models import ReservationType, Proxy, Account
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
