# # """
# # URL configuration for erp_project project.

# # The `urlpatterns` list routes URLs to views. For more information please see:
# #     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# # Examples:
# # Function views
# #     1. Add an import:  from my_app import views
# #     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# # Class-based views
# #     1. Add an import:  from other_app.views import Home
# #     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# # Including another URLconf
# #     1. Import the include() function: from django.urls import include, path
# #     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# # """
# # from django.contrib import admin
# # from django.urls import path

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# # ]

# # erp_project/urls.py

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# # Import your views for API endpoints (we will create these later)
# from students.views import StudentViewSet
# from courses.views import CourseViewSet, EnrollmentViewSet
# from finance.views import InvoiceViewSet

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'students', StudentViewSet)
# router.register(r'courses', CourseViewSet)
# router.register(r'enrollments', EnrollmentViewSet)
# router.register(r'invoices', InvoiceViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # The API URLs are now determined automatically by the router.
#     path('api/', include(router.urls)),
# ]

# erp_project/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# --- Step 1: Import the new homepage view ---
from .views import homepage

# Import your API viewsets
from students.views import StudentViewSet
from courses.views import CourseViewSet, EnrollmentViewSet
from finance.views import InvoiceViewSet

# Create a router for the API
router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    # --- Step 2: Add the path for the homepage ---
    # The empty string '' represents the root URL of the site.
    path('', homepage, name='homepage'),

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]