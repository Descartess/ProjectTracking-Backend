#serializers.py
from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from projects.models import *
from Users.models import *

class ClientSerializer(ModelSerializer):
	class Meta:
		model = Client
		fields =('id','contact_person_name','name','email','phone')

class PersonnelSerializer(ModelSerializer):
	class Meta:
		model = Personnel
		fields = ('id','first_name','last_name','email','division','level','phone')


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
		fields =('id','activity','classification','level')

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

class TaskSerializer(ModelSerializer):
	person = PersonnelSerializer()
	supervisor = PersonnelSerializer()
	activity= ActivitySerializer()
	project = ProjectSerializer()
	class Meta:
		model = Tasks
		fields =('id','task_description','person','activity','project','supervisor','due_date','status')

class TaskSaveSerializer(ModelSerializer):
	person=PrimaryKeyRelatedField(queryset=Personnel.objects.all())
	supervisor=PrimaryKeyRelatedField(queryset=Personnel.objects.all())
	project=PrimaryKeyRelatedField(queryset=Project.objects.all())
	activity=PrimaryKeyRelatedField(queryset=Activity.objects.all())
	class Meta:
		model = Tasks
		fields =('id','task_description','person','activity','project','supervisor','due_date','status')


class CommentSerializer(ModelSerializer):
	owner = PersonnelSerializer()
	task = TaskSerializer()
	class Meta:
		model = Comments
		fields = ('id','task','comment','owner','date')


class CommentSaveSerializer(ModelSerializer):
	task = PrimaryKeyRelatedField(queryset=Tasks.objects.all())
	owner = PrimaryKeyRelatedField(queryset=Personnel.objects.all())
	class Meta:
		model = Comments
		fields = ('id','task','comment','owner','date')


		