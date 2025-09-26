# students/views.py

from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

# A ViewSet for viewing and editing student instances.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # Add permissions here later for role-based access