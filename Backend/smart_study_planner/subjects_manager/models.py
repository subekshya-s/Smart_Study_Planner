from django.db import models

# Create your models here.
class Subjects(models.Model):
    subject_name  = models.CharField(max_length=100, blank=True, null=True)
    study_hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self ):
        return self.subject_name