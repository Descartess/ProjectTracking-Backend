from django.contrib import admin
from projects.models import *

admin.site.register(Project)
admin.site.register(Activity)
admin.site.register(Logs)
admin.site.register(Tasks)
admin.site.register(Comments)
