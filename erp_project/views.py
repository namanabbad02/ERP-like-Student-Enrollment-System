# erp_project/erp_project/views.py

from django.shortcuts import render

def homepage(request):
    """
    This view function handles the request to the root URL and renders
    the homepage.html template.
    """
    # The render function combines a template with a context dictionary
    # (which we can leave empty for now) and returns an HttpResponse object.
    return render(request, 'homepage.html')