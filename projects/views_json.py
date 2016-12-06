#views_json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Project
from .serializers import ProjectSerializer

class JSONResponse(HttpResponse):
	def __init__(self,data,**kwargs):
		content=JSONRenderer().render(data)
		kwargs['content_type']='application/json'
		super(JSONResponse,self).__init__(content,**kwargs)


@csrf_exempt
def Project_list(request):
	if request.method=="GET":
		projects = Project.objects.all()
		serializer =ProjectSerializer(projects,many = True)
		# return JsonResponse(serializer.data,safe=False)
		return JSONResponse(serializer.data)

@csrf_exempt
def Project_detail(request,project_id):
	try:
		project_id = int(project_id)
		project = Project.objects.get(id=project_id)
	except Project.DoesNotExist:
		return HttpResponse(status = 404)
	if request.method == "GET":
		serializer = ProjectSerializer(project)
		# return JsonResponse(serializer.data,safe=False)
		return JSONResponse(serializer.data)




