# define urls for the users app
from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns =[
# Home page for users
	url(r'^addClient/',views.addClient,name='addClient'),
	url(r'^addPersonnel/',views.addPersonnel,name='addPersonnel'),
	url(r'^register/',views.Register,name="register"),
	url(r'^logout/',views.Logout,name="logout"),
	url(r'^login/',login,{'template_name':'users/login.html'},name='login'),
	url(r'^not_authorised/',views.not_authorised,name='not_authorised')
]