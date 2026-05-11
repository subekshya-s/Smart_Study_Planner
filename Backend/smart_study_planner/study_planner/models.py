from django.db import models
from subjects_manager.models import Subjects
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
class StudyPlanner(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    completed = models.BooleanField(default=False)
     
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("end_time must be after start_time")
    def __str__(self):
        return f"{self.subject.subject_name} - {self.date}"