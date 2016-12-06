from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created =False,**kwargs):
	if created:
		Token.objects.create(user=instance)
		

class Personnel(models.Model):
	ADMIN='Administration'
	MARKETING='Marketing'
	ENGINEERING='Engineering'
	FABRICATION='Fabrication'
	
	DIVISIONS = (
		(ADMIN,'Administration'),
		(MARKETING,'Marketing'),
		(ENGINEERING,'Engineering'),
		(FABRICATION,'Fabrication'),
		)
	Default = 'Default'
	Supervisor = 'Supervisor'
	LEVELS = (
		(Default,'Default'),
		(Supervisor,'Supervisor'),
		)
	user =models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	email = models.EmailField()
	division = models.CharField(max_length=20,choices = DIVISIONS,default=ENGINEERING)
	level= models.CharField(max_length=20,choices=LEVELS,default=Default)
	phone = models.BigIntegerField()

	def __unicode__(self):
		return "%s %s "%(self.first_name, self.last_name)


    
    
class Client(models.Model):
	user =models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
	name = models.CharField(max_length=100)
	contact_person_name= models.CharField(max_length=100)
	email=models.EmailField()
	phone = models.BigIntegerField()
	def __unicode__(self):
		return self.name


   