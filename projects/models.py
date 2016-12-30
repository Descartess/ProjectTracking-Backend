from __future__ import unicode_literals
from Users.models import Client,Personnel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from channels import Group
import json
from rest_framework.serializers import ModelSerializer

class Project(models.Model):
	A='A';B='B';C='C';D='D';E='E';F='F';G='G';
	H='H';I='I';J='J';K='K';L='L';M='M';N='N';
	O='O';P='P';Q='Q';R='R';S='S';T='T';U='U';
	V='V';W='W';X='X';Y='Y';Z='Z'
	REVISIONS=(
		(A,'A'),(B,'B'),(C,'C'),(D,'D'),(E,'E'),(F,'F'),(G,'G'),(H,'H'),
		(I,'I'),(J,'J'),(K,'K'),(L,'L'),(M,'M'),(N,'N'),(O,'O'),(P,'P'),
		(Q,'Q'),(R,'R'),(S,'S'),(T,'T'),(U,'U'),(V,'V'),(W,'W'),(X,'X'),
		(Y,'Y'),(Z,'Z'),
		)
 	COMP = "Completed" 
 	PROG = "In Progress" 
 	STATUS=((COMP,"Completed"),(PROG,"In Progress"))
	name = models.CharField(max_length=100)
	proj_id= models.IntegerField()
	revision = models.CharField(max_length=1,choices= REVISIONS, default = A)
	owner=models.ForeignKey(Client)
	date=models.DateField(auto_now_add=True)
	status = models.CharField(max_length=15,choices=STATUS,default=PROG)
	def __unicode__(self):
		return self.name


class Activity(models.Model):
	PROJ='Projects Department'
	MARKETING='Marketing'
	ENGINEERING='Engineering'
	FABRICATION='Fabrication'
	CLIENT='Client'

	DIVISIONS = (
		(PROJ,'Projects Department'),
		(MARKETING,'Marketing'),
		(ENGINEERING,'Engineering'),
		(FABRICATION,'Fabrication'),
		(CLIENT,'Client')
		)

	activity = models.CharField(max_length=100)
	classification = models.CharField(max_length=20,choices=DIVISIONS,default=PROJ)
	level = models.IntegerField()
	def __unicode__(self):
		return self.activity
	class Meta:
		verbose_name='Activity'
		verbose_name_plural= 'Activities'

class Logs(models.Model):
	project = models.ForeignKey(Project)
	activity = models.ForeignKey(Activity)
	date=models.DateTimeField(auto_now_add=True)
	person=models.ForeignKey(Personnel)
	proj_rev=models.CharField(max_length=1)

	def __unicode__(self):
		return "%s %s"%(self.project,self.activity)


class Tasks(models.Model):
	task_description = models.CharField(max_length=100)
	project = models.ForeignKey(Project)
	activity = models.ForeignKey(Activity)
	person = models.ForeignKey(Personnel,related_name='person')
	supervisor = models.ForeignKey(Personnel,related_name='supervisor')
	due_date = models.DateField(null=True,blank=True)
	date_added = models.DateField(auto_now_add=True)
	status = models.IntegerField()

	def __unicode__(self):
		return "%s %s %s "%(self.task_description,self.project,self.activity)

class Comments(models.Model):
	task= models.ForeignKey(Tasks)
	comment = models.TextField()
	owner = models.ForeignKey(Personnel)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "%s %s"%(self.task,self.comment)


class MProjectSerializer(ModelSerializer):
	class Meta:
		model = Project
		fields =('id','name','proj_id','revision','date','status')

class MActivitySerializer(ModelSerializer):
	class Meta:
		model =Activity
		fields =('id','activity','classification','level')

class MLogsSerializer(ModelSerializer):
	project = MProjectSerializer()
	activity= MActivitySerializer()
	class Meta:
		model =Logs
		fields = ('id','project','activity','date',)

@receiver(post_save,sender = Logs)
def send_logs_notifications(sender,instance,created = False,**kwargs):
	if created:
		serializer = MLogsSerializer(instance)
		Group("logs").send({"text":json.dumps(serializer.data)})
	


