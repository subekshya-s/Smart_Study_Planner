from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PDFUpload, QuizResult
from subjects_manager.models import Subjects
from .utils import extract_pdf_text, generate_quiz, get_weak_topics
# Create your views here.

class UploadPDFView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        pdf_file = request.FILES.get('pdf')
        subject_id = request.data.get('subject_id')

        if not pdf_file or not subject_id:
            return Response(
                {'error': 'PDF file and subject_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subject = Subjects.objects.get(id=subject_id, user=request.user)
        except Subjects.DoesNotExist:
            return Response(
                {'error': 'Subject not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        extracted_text = extract_pdf_text(pdf_file)

        if not extracted_text.strip():
            return Response(
                {'error': 'Could not extract text. Please upload a text based PDF'},
                status=status.HTTP_400_BAD_REQUEST
            )

        pdf_upload = PDFUpload.objects.create(
            user=request.user,
            subject=subject,
            file_name=pdf_file.name,
            extracted_text=extracted_text
        )

        return Response({
            'message': 'PDF uploaded successfully',
            'pdf_id': pdf_upload.id,
            'file_name': pdf_upload.file_name,
            'subject': subject.subject_name
        }, status=status.HTTP_201_CREATED)
             
            
class GenerateQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pdf_id = request.data.get('pdf_id')

        if not pdf_id:
            return Response(
                {'error': 'pdf_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pdf = PDFUpload.objects.get(id=pdf_id, user=request.user)
        except PDFUpload.DoesNotExist:
            return Response(
                {'error': 'PDF not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        questions = generate_quiz(pdf.extracted_text, pdf.subject.subject_name)

        return Response({
            'pdf_id': pdf.id,
            'subject': pdf.subject.subject_name,
            'questions': questions
        }, status=status.HTTP_200_OK)       
    

class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pdf_id = request.data.get('pdf_id')
        answers = request.data.get('answers')
        questions = request.data.get('questions')

        if not pdf_id or not answers or not questions:
            return Response(
                {'error': 'pdf_id, answers and questions are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pdf = PDFUpload.objects.get(id=pdf_id, user=request.user)
        except PDFUpload.DoesNotExist:
            return Response(
                {'error': 'PDF not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        score = 0
        weak_topics = []

        for i, question in enumerate(questions):
            user_answer = answers.get(str(i))
            correct_answer = question.get('correct')

            if user_answer == correct_answer:
                score += 1
            else:
                weak_topics.append(question.get('topic'))

        QuizResult.objects.create(
            user=request.user,
            subject=pdf.subject,
            pdf=pdf,
            score=score,
            total_questions=len(questions),
            weak_topics=weak_topics
        )

        return Response({
            'score': score,
            'total_questions': len(questions),
            'percentage': round((score / len(questions)) * 100),
            'weak_topics': weak_topics
        }, status=status.HTTP_200_OK)
    

class WeakTopicsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quiz_results = QuizResult.objects.filter(user=request.user)
        weak_topics = get_weak_topics(quiz_results)

        return Response({
            'weak_topics': weak_topics
        }, status=status.HTTP_200_OK)