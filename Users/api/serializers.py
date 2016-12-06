from rest_framework.serializers import ModelSerializer
from Users.models import Client,Personnel
from django.contrib.auth.models import User


class UserSerializers(ModelSerializer):
	class Meta:
		model = User
		fields =('id','username','password')

class ClientSerializers(ModelSerializer):
	class Meta:
		model = Client
		fields =('id','contact_person_name','name','email','phone')

class PersonnelSerializer(ModelSerializer):
	class Meta:
		model = Personnel
		fields = ('id','first_name','last_name','email','division','level','phone')

