from rest_framework import serializers
from .models import TimetableEntry

class TimetableEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableEntry
        fields = ["id", "user", "day_of_week", "hour", "content", "created_at"]
        read_only_fields = ["id", "user", "created_at"]