# courses/models.py

from django.db import models
from students.models import Student
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection

class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A student can only enroll in the same course once
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
@receiver(post_save, sender=Enrollment)
def create_invoice_on_enrollment(sender, instance, created, **kwargs):
    """
    A signal receiver that runs every time an Enrollment is saved.
    It triggers the invoice generation stored procedure only if a new enrollment
    is being created.
    """
    # The 'created' flag is True only on the first save (i.e., creation).
    # This prevents creating a new invoice every time an enrollment is updated.
    if created:
        print("✅ post_save signal received for a new Enrollment.")
        try:
            student_id = instance.student.student_id
            course_id = instance.course.course_id
            print(f"   -> Extracted IDs. Student ID: '{student_id}', Course ID: '{course_id}'")

            with connection.cursor() as cursor:
                print("   -> Calling stored procedure: GENERATE_INVOICE_FOR_ENROLLMENT")
                cursor.callproc('GENERATE_INVOICE_FOR_ENROLLMENT', [student_id, course_id])
                print("   -> Stored procedure executed successfully!")

        except Exception as e:
            print(f"❌ ERROR in post_save signal handler: {e}")