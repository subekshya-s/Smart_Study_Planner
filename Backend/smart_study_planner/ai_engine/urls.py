from django.urls import path
from .views import UploadPDFView, GenerateQuizView, SubmitQuizView, WeakTopicsView

urlpatterns = [
    path('ai/upload-pdf/', UploadPDFView.as_view()),
    path('ai/generate-quiz/', GenerateQuizView.as_view()),
    path('ai/submit-quiz/', SubmitQuizView.as_view()),
    path('ai/weak-topics/', WeakTopicsView.as_view()),
]