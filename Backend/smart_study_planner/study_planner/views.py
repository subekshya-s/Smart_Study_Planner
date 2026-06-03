from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from study_planner.models import StudyPlanner
from study_planner.serializer import StudyPlannerSerializer

# Create your views here.
class StudyPlannerViewSet(ModelViewSet):
    serializer_class = StudyPlannerSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return StudyPlanner.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        