from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TimetableEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=[
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ])
    hour = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    content = models.TextField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.day_of_week} {self.hour}:00 - {self.content}"


class BookingRequest(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_requests")
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    status = models.CharField(max_length=20, default="pending")  
    day_of_week = models.CharField(max_length=9, choices=[
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ])
    hour = models.IntegerField()
    content = models.TextField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s settings"
