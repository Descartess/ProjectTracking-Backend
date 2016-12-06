# Define the urls for the project
from django.conf.urls import url
from . import views,views_json

urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^project/add/',views.addProject,name='AddProject'),
	url(r'^project/(?P<project_id>\d+)/$',views.viewProject,name='viewProject'),
	url(r'^project/proceed/(?P<project_id>\d+)/$',views.Proceed,name='Proceed'),
	url(r'^project/search/$',views.Search,name='Search'),
	
]