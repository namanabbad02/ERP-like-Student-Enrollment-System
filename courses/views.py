# courses/views.py

from django.db import connection # Required to call raw SQL or stored procedures
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer

# --- Course ViewSet ---
# Provides the API endpoints for creating, viewing, updating, and deleting courses.
class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    Access should be restricted to administrative users.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # Only allow authenticated users who are staff (admins) to manage courses.
    permission_classes = [permissions.IsAdminUser]


# --- Enrollment ViewSet ---
# Provides the API endpoints for managing student enrollments.
class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for student enrollments.
    - Students can view their own enrollments.
    - Admins can manage all enrollments.
    - **Crucially, creating a new enrollment triggers an invoice.**
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the queryset to only show enrollments for the requesting user
        if they are not an admin/staff member.
        """
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        # Assuming the user is a student and has a related 'student' profile
        if hasattr(user, 'student'):
            return Enrollment.objects.filter(student=user.student)
        return Enrollment.objects.none()

    # def perform_create(self, serializer):
    #     """
    #     Overrides the default create behavior to call the Oracle stored procedure
    #     after a new enrollment is successfully saved.
    #     """
    #     # First, save the new enrollment object to the database.
    #     enrollment = serializer.save()

    #     # --- Trigger Invoice Generation ---
    #     # After saving, get the required IDs for the stored procedure.
    #     student_id = enrollment.student.student_id
    #     course_id = enrollment.course.course_id

    #     try:
    #         # Use Django's database connection to get a cursor.
    #         with connection.cursor() as cursor:
    #             # Call the PL/SQL stored procedure to generate the invoice.
    #             # cursor.callproc() takes the procedure name and a list of parameters.
    #             cursor.callproc('GENERATE_INVOICE_FOR_ENROLLMENT', [student_id, course_id])
    #         print(f"Successfully called invoice generation for student {student_id} and course {course_id}.")
    #     except Exception as e:
    #         # If the stored procedure fails, we should ideally handle the error.
    #         # For example, we could delete the enrollment that was just created to
    #         # maintain data consistency, or flag it for manual review.
    #         print(f"Error calling stored procedure: {e}")
    #         # Consider raising a validation error or returning a specific error response.

    def perform_create(self, serializer):
        """
        Overrides the default create behavior to call the Oracle stored procedure
        after a new enrollment is successfully saved.
        """
        print("--- Starting perform_create for new enrollment ---")
        try:
            # First, save the new enrollment object to the database.
            enrollment = serializer.save()
            print(f"✅ Step 1: Enrollment object saved successfully. ID: {enrollment.id}")

            # After saving, get the required IDs for the stored procedure.
            student_id = enrollment.student.student_id
            course_id = enrollment.course.course_id
            print(f"✅ Step 2: Extracted IDs. Student ID: '{student_id}', Course ID: '{course_id}'")

            # Use Django's database connection to get a cursor.
            with connection.cursor() as cursor:
                print("✅ Step 3: Database cursor created. Calling stored procedure...")
                # Call the PL/SQL stored procedure to generate the invoice.
                cursor.callproc('GENERATE_INVOICE_FOR_ENROLLMENT', [student_id, course_id])
                print("✅ Step 4: Stored procedure executed successfully!")

        except Exception as e:
            # This block will catch any error during the process.
            print("❌ AN ERROR OCCURRED! ❌")
            print(f"Error details: {e}")
        
        print("--- Finished perform_create ---")