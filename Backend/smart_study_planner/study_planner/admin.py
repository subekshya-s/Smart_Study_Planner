from django.contrib import admin

# Register your models here.
from django.contrib import admin
from study_planner.models import StudyPlanner
from subjects_manager.models import  Subjects

admin.site.register(StudyPlanner)