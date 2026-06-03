from django.db import models
from django.contrib.auth.models import User
from subjects_manager.models import Subjects

class PDFUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    extracted_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.file_name}"

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDFUpload, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    weak_topics = models.JSONField(default=list)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.subject} - {self.score}/{self.total_questions}"