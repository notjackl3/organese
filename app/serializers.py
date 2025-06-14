from rest_framework import serializers
from .models import Timetable, TimetableEntry


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ["id", "user", "name", "is_public", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class TimetableEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableEntry
        fields = ["id", "timetable", "day_of_week", "hour", "content", "created_at"]
        read_only_fields = ["id", "timetable", "created_at"]