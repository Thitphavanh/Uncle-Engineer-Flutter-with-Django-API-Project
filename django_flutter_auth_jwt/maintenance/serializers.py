from rest_framework import serializers
from .models import Maintenance


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = (
            "id",
            "transaction_id",
            "name",
            "department",
            "machine",
            "proplem",
            "tel",
        )
