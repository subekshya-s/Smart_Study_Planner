from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Subjects
from .serializers import SubjectsSerializer
# Create your views here.
class SubjectsViewSet(ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer