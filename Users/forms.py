#forms.py
from django import forms
from . models import Client,Personnel
class ClientForm(forms.ModelForm):
	class Meta:
		model= Client
		fields=['name','contact_person_name','email','phone']


class PersonnelForm(forms.ModelForm):
	class Meta:
		model= Personnel
		fields = ['first_name','last_name','email','division','phone','level']
		