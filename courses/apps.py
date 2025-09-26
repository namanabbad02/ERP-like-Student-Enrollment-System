# courses/apps.py

from django.apps import AppConfig

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    # --- ADD THIS METHOD ---
    def ready(self):
        """
        This method is called when the app is loaded.
        We import our signals here to ensure they are connected.
        """
        import courses.models # This line will discover and connect the receiver