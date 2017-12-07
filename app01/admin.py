from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Classes)
admin.site.register(models.UserInfo)
admin.site.register(models.Questionnaire)
admin.site.register(models.Question)
admin.site.register(models.Option)
admin.site.register(models.Result)