from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class ContactForm(forms.Form):
	name= forms.CharField(max_length=45)
	email= forms.EmailField()
	message= forms.CharField(widget=forms.Textarea)


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ClientForm(ModelForm):
	class Meta:
		model= Client
		fields= '__all__'
		exclude=['user']

class ClientUserForm(ModelForm):
	class Meta:
		model= Client
		fields= '__all__'
		exclude= ['user', 'account_number', 'account_type', 'account_status', 'deposit', 'uncleared_balance', 'total_loan', 'date_created', 'account_currency', 'transfer_pin']



