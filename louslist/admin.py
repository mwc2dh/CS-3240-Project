from django.contrib import admin
from .models import Profile, Course, Section, Meeting

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Meeting)