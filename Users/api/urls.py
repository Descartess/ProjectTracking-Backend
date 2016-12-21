from django.conf.urls import url
from django.contrib import admin
from Users.api.views import *
# from rest_framework.authtoken import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
   # url(r'^$',ProjectListAPIView.as_view(), name ='list'),
   url(r'^staff/$',PersonnelList.as_view()),
   url(r'^client/$',CLientList.as_view()),
   url(r'^api-token-auth/(?P<pk>\d+)/$',ProjectAuthToken.as_view()),
   # url(r'^$',ProjectList.as_view()),
   url(r'^staff/(?P<pk>\d+)/$',PersonnelDetail.as_view()),
   url(r'^client/(?P<pk>\d+)/$',ClientDetail.as_view()),
   # url(r'^search/$',SearchList.as_view()),
 ]

urlpatterns = format_suffix_patterns(urlpatterns)
