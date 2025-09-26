# courses/serializers.py

from rest_framework import serializers
from .models import Course, Enrollment

# --- Course Serializer ---
# This handles the conversion of Course model instances to JSON format.
class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    """
    class Meta:
        model = Course
        # Includes all fields from the Course model in the API representation.
        fields = '__all__'


# --- Enrollment Serializer ---
# This handles the serialization of Enrollment model instances.
class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.

    This serializer provides a detailed, read-only representation of the student
    and course for GET requests, making the API response more informative. For POST
    requests (creating an enrollment), it expects the primary keys for student and course.
    """
    # For read operations (like GET), display the string representation of the
    # student and course models (e.g., "Rahul Sharma", "Data Structures").
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    # For write operations (like POST), we need to specify the fields that
    # the client should send. These are not read-only. We expect the client
    # to send the primary keys (student_id and course_id).
    student_id = serializers.CharField(write_only=True, source='student')
    course_id = serializers.CharField(write_only=True, source='course')

    class Meta:
        model = Enrollment
        # The 'fields' list defines what is included in the API response.
        fields = ['id', 'student', 'course', 'semester', 'enrollment_date', 'student_id', 'course_id']

        # 'read_only_fields' are fields that are not expected from the client
        # when creating or updating, like the auto-generated enrollment_date.
        read_only_fields = ['enrollment_date']

    def create(self, validated_data):
        # This method handles the creation of a new Enrollment instance.
        # It pops the student and course objects from validated_data and passes them
        # directly to the Enrollment.objects.create method.
        return Enrollment.objects.create(**validated_data)