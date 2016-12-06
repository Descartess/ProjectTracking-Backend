from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import *
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from Users.models import *
from projects.models import *

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

@login_required
def index(request):
	user=request.user.username
	try:
		c=Personnel.objects.get(email=user)
		logs = Logs.objects.all().order_by('-date')[:10]
		form= SearchForm()
		active_projects= Project.objects.filter(status__icontains="In Progress")
		mkt_log=[];proj_log=[];fab_log=[]
		eng_log=[];client_log=[]
		for projct in active_projects:
			task = Logs.objects.filter(project=projct).latest('date')
			task_level=int(task.activity.level)+1
			actv=Activity.objects.get(level=task_level)
			activ=[actv,projct]
			if actv.classification == 'Projects Department':
				proj_log.append(activ)
			elif actv.classification == 'Marketing':
				mkt_log.append(activ)
			elif actv.classification == 'Engineering':
				eng_log.append(activ)
			elif actv.classification == 'Fabrication':
				fab_log.append(activ)
			elif actv.classification == 'Client':
				client_log.append(activ)
		context = {'logs':logs,'form':form,'Eng':eng_log,'Mkt':mkt_log,'Cli':client_log,'Prj':proj_log,'Fab':fab_log}		
		return render(request,'projects/index.html',context)
	except ObjectDoesNotExist:
		try:
			client=Client.objects.get(email=user)
			projects = Project.objects.filter(owner=client).order_by('-date')
			context={'projects':projects,'client':client}
			return render(request,'projects/client.html',context)
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse('users:not_authorised'))

@mkt_login
def addProject(request):
	if request.method != "POST":
		form=ProjectForm()
		context = {'form':form}
		return render(request,'projects/addProject.html',context)
	else:
		form=ProjectForm(request.POST)
		if form.is_valid():
			c=form.save()
			proj_id=c.id
			Revision = c.revision
			stage = Activity.objects.get(level=1)
			Person = Personnel.objects.get(email=request.user.username)
			e=Logs(project=c,activity=stage,person=Person,proj_rev=Revision)
			e.save()
			return HttpResponseRedirect(reverse('projects:viewProject',kwargs={'project_id':proj_id}))

@login_required
def viewProject(request,project_id):
	# Finding number of activities in process
	num_activ=Activity.objects.count() 
	user=request.user.username
	proj_id=int(project_id)
	c= Project.objects.get(id=proj_id)
	Log_data=Logs.objects.filter(project=c)
	prg_level=[]
	for elem in Log_data:
		log_id = int(elem.activity.id)
		stage = Activity.objects.get(level=log_id)
		prg_level.append(int(stage.level))   
	lev=(max(prg_level)/float(num_activ))*100.0
	try:
		client=Client.objects.get(email=user)
		if c.owner == client:
			proj_id=int(project_id)
			logs= Logs.objects.filter(project=c).order_by('-date')
			context={'logs':logs,'Project':c,'percentage':lev}
			return render(request,'projects/viewProject.html',context)
		else:
			return HttpResponseRedirect(reverse('users:not_authorised'))
	except ObjectDoesNotExist:
		logs= Logs.objects.filter(project=c).order_by('-date')
		context={'logs':logs,'step':proj_id,'Project':c,'percentage':lev}
		return render(request,'projects/viewProject.html',context)

# @supervisor_login		
def Proceed(request,project_id):
	proj_id=int(project_id)
	c= Project.objects.get(id=proj_id)
	Person = Personnel.objects.get(email=request.user.username)
	Revision = c.revision
	log= Logs.objects.filter(project=c).latest('date')
	log_id =int(log.activity.id)
	stage = Activity.objects.get(level=log_id+1)
	e=Logs(project=c,activity=stage,person=Person,proj_rev=Revision)
	e.save()
	return HttpResponseRedirect(reverse('projects:viewProject',kwargs={'project_id':proj_id}))

@staff_login
def Search(request):
	if request.method == "POST":
		search_term =  request.POST['text_input'].strip()
		projects=Project.objects.filter(name__icontains=search_term) | Project.objects.filter(proj_id__icontains=search_term)
	context = {'search_term':search_term,'projects':projects}
	return render(request,'projects/search.html',context)