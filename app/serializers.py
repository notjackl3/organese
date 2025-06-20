from rest_framework import serializers
from .models import Timetable, TimetableEntry, BookingRequest


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


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ["id", "guest_name", "guest_email", "status", "day_of_week", "hour", "content", "created_at"]
        read_only_fields = ["id", "created_at"]
    
    def create(self, validated_data):
        timetable = self.context["timetable"]
        owner = self.context["owner"]
        return BookingRequest.objects.create(
            timetable=timetable,
            owner=owner,
            **validated_data
        )