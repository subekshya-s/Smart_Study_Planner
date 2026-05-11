from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subjects(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    subject_name  = models.CharField(max_length=100,default='Unknown')
    study_hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self ):
        return self.subject_name