from django.contrib import admin

from .models import RecipeName, PatientDetail, AudioData, PatientProperty
admin.site.register(RecipeName)
admin.site.register(PatientDetail)
admin.site.register(AudioData)
admin.site.register(PatientProperty)