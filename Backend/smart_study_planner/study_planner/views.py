from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from study_planner.models import StudyPlanner
from study_planner.serializer import StudyPlannerSerializer
from study_planner.models import StudyPlanner

# Create your views here.
class StudyPlannerViewSet(ModelViewSet):
    queryset = StudyPlanner.objects.all()
    serializer_class = StudyPlannerSerializer