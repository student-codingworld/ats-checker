from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDescriptionSerializer, JobDescription, ResumeSerializer, Resume
from .analyzer import process_resume



def home(request):
    return HttpResponse("""
        <h1>Welcome to ATS Checker!</h1>
        <p>Use the following API endpoints:</p>
        <ul>
            <li><a href="/api/jobs">/api/jobs</a></li>
            <li>/api/resume/ (POST method)</li>
        </ul>
    """)    


class JobDescriptionAPI(APIView):
    def get(self, request):
        queryset = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(queryset, many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })


class AnalyzeResumeAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            if not data.get('job_description'):
                return Response({
                    'status': False,
                    'message': 'job_description is required',
                    'data': {}
                })

            serializer = ResumeSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'errors',
                    'data': serializer.errors
                })

            serializer.save()
            _data = serializer.data
            resume_instance = Resume.objects.get(id=_data['id'])
            resume_path = resume_instance.resume.path
            data = process_resume(resume_path,
            JobDescription.objects.get(id=data.get('job_description')).job_description
            )

            return Response({
                'status': True,
                'message': 'resume analyzed',
                'data': data
            })

        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            })
