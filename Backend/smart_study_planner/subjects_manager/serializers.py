from rest_framework import serializers
from .models import Subjects

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'
        read_only_fields = ['user','created_at']