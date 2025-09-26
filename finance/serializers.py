# finance/serializers.py

from rest_framework import serializers
from .models import Invoice

# --- Invoice Serializer ---
# This class defines how the Invoice model data will be represented in the API.
# It converts complex data types, like model instances, into native Python
# datatypes that can then be easily rendered into JSON.

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.

    Includes a nested representation of the related student for richer API responses.
    This helps the client see student details without making a separate API call.
    """
    # 'student' is a ForeignKey in the model. By default, it would only show the
    # student's primary key (student_id). Using StringRelatedField displays the
    # string representation of the student object (from its __str__ method).
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Invoice
        # The '__all__' value tells the serializer to include all fields from the
        # Invoice model in the API representation.
        fields = '__all__'

        # Alternatively, you can specify fields explicitly:
        # fields = ['invoice_id', 'student', 'amount', 'status', 'date_generated', 'due_date']