#serializers.py
from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from projects.models import Project,Activity,Logs 
from Users.models import Client

class ClientSerializer(ModelSerializer):
	class Meta:
		model = Client
		fields =('id','contact_person_name','name','email','phone')


class ProjectSerializer(ModelSerializer):
	owner = ClientSerializer()
	class Meta:
		model = Project
		fields =('id','name','proj_id','revision','owner','date','status')

class ProjectSaveSerializer(ModelSerializer):
	owner = PrimaryKeyRelatedField(queryset=Client.objects.all())
	class Meta:
		model = Project
		fields =('id','name','proj_id','revision','owner','status')

class ActivitySerializer(ModelSerializer):
	class Meta:
		model =Activity
		fields =('activity','classification','level')

class LogsSerializer(ModelSerializer):
	project = ProjectSerializer()
	activity= ActivitySerializer()
	class Meta:
		model =Logs
		fields = ('id','project','activity','date',)

class LogsDetailSerializer(ModelSerializer):
	activity= ActivitySerializer()
	class Meta:
		model =Logs
		fields = ('id','activity','date',)
		