# finance/views.py

from rest_framework import viewsets, permissions
from .models import Invoice
from .serializers import InvoiceSerializer

# --- Invoice ViewSet ---
# A ViewSet in Django REST Framework provides a high-level abstraction for handling
# API operations. ModelViewSet automatically provides the full set of CRUD
# (Create, Retrieve, Update, Destroy) operations for a model.

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    This ViewSet handles listing, creating, retrieving, updating,
    and deleting invoices.
    """
    # The queryset defines the collection of objects that are available for this view.
    # Here, we are making all Invoice objects available.
    queryset = Invoice.objects.all().order_by('-date_generated')

    # The serializer_class tells the ViewSet which serializer to use for
    # converting the model instances to and from JSON.
    serializer_class = InvoiceSerializer

    # --- Role-Based Permissions (Example) ---
    # The permission_classes attribute controls who can access this API endpoint.
    # For instance, you might want only Admins and Finance Officers to view invoices.
    # (This requires a custom permission class, shown as an example below).
    # For now, we will use IsAuthenticated to ensure only logged-in users can access it.
    permission_classes = [permissions.IsAuthenticated]

    # --- Example of Custom Logic ---
    # You can override methods to add custom logic. For example, to only show
    # a student their own invoices.
    def get_queryset(self):
        """
        Optionally restricts the returned invoices to a given user,
        by filtering against a `student` query parameter in the URL.
        """
        user = self.request.user

        # If the user is a superuser or in the 'Finance Officer' group, show all invoices.
        if user.is_superuser or user.groups.filter(name='Finance Officer').exists():
            return Invoice.objects.all().order_by('-date_generated')

        # If the user is a student, only show their own invoices.
        if hasattr(user, 'student'):
            return Invoice.objects.filter(student=user.student).order_by('-date_generated')

        # Otherwise, return an empty list if the user has no associated role.
        return Invoice.objects.none()