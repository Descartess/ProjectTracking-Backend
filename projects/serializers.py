#serializers.py
from rest_framework import serializers
from .models import Project,Logs,Activity
from Users.models import Client
class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields =('id','contact_person_name','name','email')


class ProjectSerializer(serializers.ModelSerializer):
	owner = ClientSerializer()
	class Meta:
		model = Project
		fields =('id','name','proj_id','revision','owner','date','status')
