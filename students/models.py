# students/models.py

from django.db import models
from django.contrib.auth.models import User

# Extends the built-in User model to store role-specific information
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True, primary_key=True)
    contact = models.CharField(max_length=15)
    program = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
# # students/models.py

# from django.db import models
# from django.contrib.auth.models import User

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     student_id = models.CharField(max_length=10, unique=True, primary_key=True)
#     contact = models.CharField(max_length=15)
#     program = models.CharField(max_length=50)
#     year = models.IntegerField()

#     # --- REPLACE THE OLD __str__ METHOD WITH THIS ONE ---
#     def __str__(self):
#         # Try to get the user's full name. The strip() removes whitespace.
#         full_name = self.user.get_full_name().strip()
        
#         # If the full_name is not empty, return it.
#         # Otherwise, fall back to the username, which is always available.
#         return full_name if full_name else self.user.username