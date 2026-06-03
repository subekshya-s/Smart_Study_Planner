from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Subjects
from .serializers import SubjectsSerializer

class SubjectsViewSet(ModelViewSet):
    serializer_class= SubjectsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subjects.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)