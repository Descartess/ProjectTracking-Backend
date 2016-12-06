# #views.py
from Users.models import *
from Users.api.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404

from rest_framework.response import Response 
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken

class PersonnelList(APIView):
	# authentication_classes = (TokenAuthentication,)
	def get(self,request,format =None):
		queryset = Personnel.objects.all()
		serializer =PersonnelSerializer(queryset,many = True)
		return Response(serializer.data)

	def post(self,request,format=None):
		serializer = PersonnelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

class PersonnelDetail(APIView):
	# authentication_classes = (TokenAuthentication,)
	def get_object(self,pk):
		try:
			return Personnel.objects.get(pk=pk)
		except  ObjectDoesNotExist:
			raise Http404

			
	def get(self,request,pk,format = None):
		person = self.get_object(pk)
		serializer = PersonnelSerializer(person)
		return Response(serializer.data)

	
	def put(self,request,pk,format = None):
		person = self.get_object(pk=pk)
		serializer = PersonnelSerializer(person,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializers.data)
		return Response(serializers.errors)


class CLientList(APIView):
	"""
	Displays all clients 
	"""
	authentication_classes = (TokenAuthentication,)
	def get(self,request,format =None):
		queryset = Client.objects.all()
		serializer =ClientSerializers(queryset,many = True)
		return Response(serializer.data)

	def post(self,request,format=None):
		serializer = ClientSerializers(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)


class ClientDetail(APIView):
	"""
	Displays Invididual Client Detail
	"""
	# authentication_classes = (TokenAuthentication,)
	def get_object(self,pk):
		try:
			return Client.objects.get(pk=pk)
		except ObjectDoesNotExist:
			raise Http404
	def get(self,request,pk,format = None):
		person = self.get_object(pk)
		serializer = ClientSerializers(person)
		return Response(serializer.data)

	
	def put(self,request,pk,format = None):
		person = self.get_object(pk=pk)
		serializer = ClientSerializers(person,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializers.data)
		return Response(serializers.errors)

class ProjectAuthToken(ObtainAuthToken):
	
	    def post(self,request,pk,*args, **kwargs):
	    	#  Register code here
	    	if int(pk) == 1:
	    		username = request.data['username']
	    		try:
	    			person=Personnel.objects.get(email__iexact=username)
	    			serializer = UserSerializers(data=request.data)
	    			if serializer.is_valid():
	    				user=serializer.save()
    					persondata = PersonnelSerializer(person)
    					token, created = Token.objects.get_or_create(user=user)
        				return Response({'token': token.key, 'user':persondata.data,'is_staff':'false'})
	    		except  ObjectDoesNotExist:
	    			try:
	    				person=Client.objects.get(email__iexact=username)
	    				serializer = UserSerializers(data=request.data)
	    				if serializer.is_valid():
	    					user=serializer.save()
	    					persondata = ClientSerializers(person)
	    					token, created = Token.objects.get_or_create(user=user)
	        				return Response({'token': token.key, 'user':persondata.data,'is_staff':'false'})

	    			except ObjectDoesNotExist:
	    				return Response({'value':'not caught  '})
	    	
	    	# Login Code 

	        serializer = self.serializer_class(data=request.data)
	        serializer.is_valid(raise_exception=True)
	        user = serializer.validated_data['user']
	        token, created = Token.objects.get_or_create(user=user)
	        userdata = user.username
	        try:
	        	person=Personnel.objects.get(email__iexact=userdata)
	        	persondata = PersonnelSerializer(person)
	        	return Response({'token': token.key, 'user':persondata.data,'is_staff':'true'})
	        except ObjectDoesNotExist:
	        	person=Client.objects.get(email__iexact=userdata)
	        	persondata = ClientSerializers(person)
	        	return Response({'token': token.key, 'user':persondata.data,'is_staff':'false'})
	        