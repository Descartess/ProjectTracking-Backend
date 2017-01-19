
from django.conf.urls import url
from django.contrib import admin
from projects.api.views import *

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
   # url(r'^$',ProjectListAPIView.as_view(), name ='list'),
   url(r'^$',ProjectList.as_view()),
   url(r'^logs/$',LogList.as_view()),
   url(r'^notifs/$',Notifications.as_view()),
   # url(r'^$',ProjectList.as_view()),
   url(r'^(?P<pk>\d+)/$',ProjectDetail.as_view()),
   url(r'^update/(?P<pk>\d+)/$',UpdateProjectProgess.as_view()),
   url(r'^create/(?P<pk>\d+)/$',CreateProjectCLient.as_view()),
   url(r'^viewTask/(?P<pk>\d+)/(?P<actv_id>\d+)/$',TaskList.as_view()),
   url(r'^viewPersonnelTask/(?P<pk>\d+)/$',PersonnelTaskList.as_view()),
   url(r'^createTask/(?P<pk>\d+)/$',TaskSaveList.as_view()),
   url(r'^search/$',SearchList.as_view()),
   url(r'^verbs/$',VerbsList.as_view()),
 ]

urlpatterns = format_suffix_patterns(urlpatterns)