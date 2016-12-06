#permissions.py
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from Users.models import *
from projects.models import *


class PersonnelPermission(BasePermission):
	def has_permission(self,request,view):
		user = request.user
		if user.is_authenticated:
			try:
				c=Personnel.objects.get(email=user.username)
				return True 
			except ObjectDoesNotExist:
				return False
		else:
			return False
	

class SupervisorPermission(BasePermission):
	def has_permission(self,request,view):
		user = request.user
		if user.is_authenticated:
			try:
				c=Personnel.objects.get(email=user.username)
				if c.level =="Supervisor":
					return True
				else:
					return False 
			except ObjectDoesNotExist:
				return False
		else:
			return False

class MarketingPermission(BasePermission):
	def has_permission(self,request,view):
		user = request.user
		if user.is_authenticated:
			try:
				c=Personnel.objects.get(email=user.username)
				if c.division =="Marketing":
					return False
				else:
					return False 
			except ObjectDoesNotExist:
				return False
		else:
			return False

			

