# #views.py
from projects.models import *
from projects.api.serializers import *
from Users.api.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView 
from projects.api.permissions import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

class ProjectList(APIView):
	""" 
	List all Projects
	
	"""
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def get(self,request,format=None):
		user = request.user.username
		try:
			c=Personnel.objects.get(email__iexact=user)
			queryset = Project.objects.all()
			serializer =ProjectSerializer(queryset,many = True)
			return Response(serializer.data)
		except ObjectDoesNotExist:
			try:
				client=Client.objects.get(email__iexact=user)
				queryset = Project.objects.filter(owner=client).order_by('-date')
				serializer =ProjectSerializer(queryset,many = True)
				return Response(serializer.data)
			except ObjectDoesNotExist:
				pass


class CreateProjectCLient(APIView):
	"""
	Create new projects  
	"""
	def post(self,request,pk,format=None):
		if int(pk) == 0:
			data = request.data
			client_data=data["client"]
			project_data=data["project"]
			serializer0 = ClientSerializers(data=client_data)

			if serializer0.is_valid():
				user = serializer0.save()
				project_data["owner"] = user.id
				serializer = ProjectSaveSerializer(data=project_data)
				if serializer.is_valid():
					project=serializer.save()
					Revision = project.revision
					stage = Activity.objects.get(level=1)
					Person = Personnel.objects.get(email__iexact=request.user.username)
					e=Logs(project=project,activity=stage,person=Person,proj_rev=Revision)
					e.save()
					return Response(serializer.data)
			else:
				return Response({"errors":serializer0.errors})
		elif int(pk)==1:
			client_data=data["client"]
			project_data=data["project"]
			project_data["owner"] = int(client_data.id)
			serializer = ProjectSaveSerializer(data=project_data)
			if serializer.is_valid():
				project=serializer.save()
				Revision = project.revision
				stage = Activity.objects.get(level=1)
				Person = Personnel.objects.get(email__iexact=request.user.username)
				e=Logs(project=project,activity=stage,person=Person,proj_rev=Revision)
				e.save()
				return Response(serializer.data)
			return Response(serializer.errors)

class ProjectDetail(APIView):
	"""
	Displays project details 
	"""
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def get_object(self,pk):
		try:
			return Project.objects.get(pk=pk)
		except ObjectDoesNotExist:
			raise Http404

	def get(self,request,pk,format=None):
		
		project = self.get_object(pk)
		serializer = ProjectSerializer(project)
		Log_data=Logs.objects.filter(project=project).order_by('-date')

		serializer_2 = LogsDetailSerializer(Log_data,many=True)
		# Finding number of activities in process
		num_activ=Activity.objects.count() 

        # Start computing % completion
		prg_level=[]
		for elem in Log_data:
			log_id = int(elem.activity.id)
			stage = Activity.objects.get(level=log_id)
			prg_level.append(int(stage.level))   
		lev=(max(prg_level)/float(num_activ))*100.0

		# end computing % completion

		data ={"project":serializer.data,"percentage":lev,"logs":serializer_2.data}

		return Response(data)


	def put(self,request,format =None):
		serializer = ProjectSerializer(request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

class SearchList(APIView):
	"""
	Returns a list of items from the search query
	"""
	permission_classes = (IsAuthenticated,PersonnelPermission,)
	
	authentication_classes = (TokenAuthentication,)
	def post(self,request,format = None):
		search_term =  request.data["search_term"]
		projects=Project.objects.filter(name__icontains=search_term) | Project.objects.filter(proj_id__icontains=search_term)
		serializer=ProjectSerializer(projects,many=True)
		return Response(serializer.data)


class LogList(APIView):
	"""
	Display Project Logs 

	"""
	permission_classes = (IsAuthenticated,PersonnelPermission,)
	
	authentication_classes = (TokenAuthentication,)
	def get(self,request,format = None):
		active_projects= Project.objects.filter(status__icontains="In Progress")
		log_data =[]
		for projct in active_projects:
			task = Logs.objects.filter(project=projct).latest('date')
			serializer=LogsSerializer(task)
			log_data.append(serializer.data)
		return Response(log_data)


class Notifications(APIView):
	"""
	Display notifications in the respective project departments.
	"""
	permission_classes = (IsAuthenticated,PersonnelPermission,)

	authentication_classes = (TokenAuthentication,)

	def get(self,request,format = None):
		active_projects= Project.objects.filter(status__icontains="In Progress")
		mkt_log=[];proj_log=[];fab_log=[]
		eng_log=[];client_log=[]
		for projct in active_projects:
			task = Logs.objects.filter(project=projct).latest('date')
			task_level=int(task.activity.level)+1
			actv=Activity.objects.get(level=task_level)
			if actv.classification == 'Projects Department':
				activ = ActivitySerializer(actv)
				dat = activ.data
				dat["name"]=projct.name; dat["id"]=projct.id;
				proj_log.append(dat)
			elif actv.classification == 'Marketing':
				activ = ActivitySerializer(actv)
				dat = activ.data
				dat["name"]=projct.name; dat["id"]=projct.id;
				mkt_log.append(dat)
			elif actv.classification == 'Engineering':
				activ = ActivitySerializer(actv)
				dat = activ.data
				dat["name"]=projct.name; dat["id"]=projct.id;
				eng_log.append(dat)
			elif actv.classification == 'Fabrication':
				activ = ActivitySerializer(actv)
				dat = activ.data
				dat["name"]=projct.name; dat["id"]=projct.id;
				fab_log.append(dat)
			elif actv.classification == 'Client':
				activ = ActivitySerializer(actv)
				dat = activ.data
				dat["name"]=projct.name; dat["id"]=projct.id;
				client_log.append(dat)	

		data = {"project_dept":proj_log,"marketing_dept":mkt_log,"Eng_dept":eng_log,"Fab_dept":fab_log}
		return Response(data)


class UpdateProjectProgess(APIView):
	"""
	 Takes project to next level  project details 

	"""

	permission_classes = (PersonnelPermission,)
	authentication_classes = (TokenAuthentication,)
	def get_object(self,pk):
		try:
			return Project.objects.get(pk=pk)
		except ObjectDoesNotExist:
			raise Http404

	def get(self,request,pk,format=None):
		
		project = self.get_object(pk)

		#  Updating data about a project 

		Person = Personnel.objects.get(email__iexact=request.user.username)
		Revision = project.revision
		log= Logs.objects.filter(project=project).latest('date')
		log_id =int(log.activity.id)
		stage = Activity.objects.get(level=log_id+1)
		e=Logs(project=project,activity=stage,person=Person,proj_rev=Revision)
		e.save()

		# Retrieving data  from updated project.

		serializer = ProjectSerializer(project)
		Log_data=Logs.objects.filter(project=project).order_by('-date')

		serializer_2 = LogsDetailSerializer(Log_data,many=True)
		# Finding number of activities in process
		num_activ=Activity.objects.count() 

        # Start computing % completion
		prg_level=[]
		for elem in Log_data:
			log_id = int(elem.activity.id)
			stage = Activity.objects.get(level=log_id)
			prg_level.append(int(stage.level))   
		lev=(max(prg_level)/float(num_activ))*100.0

		# end computing % completion

		data ={"project":serializer.data,"percentage":lev,"logs":serializer_2.data}

		return Response(data)



