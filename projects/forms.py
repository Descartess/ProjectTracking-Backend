# forms for the projects
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields=['name','proj_id','revision','owner']

class SearchForm(forms.Form):
	text_input = forms.CharField(label='Search Projects',max_length=200)

