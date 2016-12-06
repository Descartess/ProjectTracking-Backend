from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout,authenticate,login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import *
from . forms import *

def staff_login(function):
	def wrapper(request,*args,**kwargs):
		user = request.user
		if user.is_authenticated:
			try:
				c=Personnel.objects.get(email=user.username)
				return function(request,*args,**kwargs)
			except ObjectDoesNotExist:
				return HttpResponseRedirect(reverse('users:not_authorised'))
		else:
			return HttpResponseRedirect('users/login')
	return wrapper

def supervisor_login(function):
	def wrapper(request,*args,**kwargs):
		user = request.user
		if user.is_authenticated:
			try:
				c=Personnel.objects.get(email=user.username)
				if c.level =="Supervisor":
					pass
				else:
					return HttpResponseRedirect(reverse('users:not_authorised'))					
				return function(request,*args,**kwargs)
			except ObjectDoesNotExist:
				return HttpResponseRedirect(reverse('users:not_authorised'))
		else:
			return HttpResponseRedirect('users/login')
	return wrapper

def mkt_login(function):
	def wrapper(request,*args,**kwargs):
		user = request.user
		if user.is_authenticated:
			try:
				c=Personnel.objects.get(email=user.username)
				if c.division =="Marketing":
					pass
				else:
					return HttpResponseRedirect(reverse('users:not_authorised'))					
				return function(request,*args,**kwargs)
			except ObjectDoesNotExist:
				return HttpResponseRedirect(reverse('users:not_authorised'))
		else:
			return HttpResponseRedirect('users/login')
	return wrapper

def client_login(function):
	def wrapper(function,*args,**kwargs):
		user =  request.user
		if user.is_authenticated:
			try:
				c=Client.objects.get(email=user.username)
				return function(request,*args,**kwargs)
			except ObjectDoesNotExist:
				return HttpResponseRedirect(reverse('users:not_authorised'))
		else:
			return HttpResponseRedirect('users/login')
	return wrapper

@mkt_login
def addClient(request):
	if request.method != "POST":
		form=ClientForm()
		context={'form':form}
		return render(request,'users/addClient.html',context)
	else:
		form=ClientForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('projects:AddProject'))

@supervisor_login
def addPersonnel(request):
	if request.method != "POST":
		form=PersonnelForm()
		context={'form':form}
		return render(request,'users/addPersonnel.html',context)
	else:
		form=PersonnelForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('projects:index'))
	

def Register(request):
	if request.method != "POST":
		form =UserCreationForm()
		context={"form":form}
		return render(request,'users/register.html',context)
	else:
		form=UserCreationForm(data=request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			try:
				c=Client.objects.get(email=username)
				new_user=form.save()
				c.user=new_user
				c.save()
				authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
				login(request,authenticated_user)
				return HttpResponseRedirect(reverse('projects:index'))
			except ObjectDoesNotExist:
				try:
					c=Personnel.objects.get(email=username)
					new_user=form.save()
					c.user=new_user
					c.save()
					authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
					login(request,authenticated_user)
					return HttpResponseRedirect(reverse('projects:index'))
				except ObjectDoesNotExist:
					context={"form":form,'username':'The Username does not exist: %s'%username}
					return render(request,'users/register.html',context)
		else:
			context={"form":form}
			return render(request,'users/register.html',context)

@login_required
def Logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('projects:index'))

def not_authorised(request):
	username=request.user.username
	context = {'username':username}
	return render(request,'users/500.html',context)


	