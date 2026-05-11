from rest_framework import serializers
from study_planner.models import StudyPlanner
from subjects_manager.models import  Subjects

class StudyPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlanner
        fields = "__all__"