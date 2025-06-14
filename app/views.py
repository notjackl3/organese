from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import TimetableEntry, UserSettings, BookingRequest
from .serializers import TimetableEntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class TimetableEntryViewSet(viewsets.ModelViewSet):
    queryset = TimetableEntry.objects.all()
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TimetableEntryList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        entries = TimetableEntry.objects.filter(user=request.user)
        serializer = TimetableEntrySerializer(entries, many=True) # make some attributes read-only
        return Response(serializer.data)

    def post(self, request):
        serializer = TimetableEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimetableEntryDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(TimetableEntry, pk=pk, user=user)

    def get(self, request, pk):
        entry = self.get_object(pk, request.user)
        serializer = TimetableEntrySerializer(entry)
        return Response(serializer.data)

    def put(self, request, pk):
        entry = self.get_object(pk, request.user)
        serializer = TimetableEntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        entry = self.get_object(pk, request.user)
        serializer = TimetableEntrySerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        entry = self.get_object(pk, request.user)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TimetableEntryLookup(APIView):
    def post(self, request):
        day = request.data.get('day_of_week')
        hour = request.data.get('hour')
        print("this runs")
        try:
            entry = TimetableEntry.objects.get(
                day_of_week=day,
                hour=hour,
                user_id = request.user.id
            )
            return Response({"pk": entry.pk}, status=status.HTTP_200_OK)
        except TimetableEntry.DoesNotExist:
            return Response({"error": "No entry found."}, status=status.HTTP_404_NOT_FOUND)
        except TimetableEntry.MultipleObjectsReturned:
            entries = TimetableEntry.objects.filter(
                day_of_week=day, 
                hour=hour, 
                user_id = request.user.id)
            print(entries.values())
            return Response({"multiple": True, "pk": entries.values()}, status=status.HTTP_200_OK)
        

@api_view(["GET"])
def entries_by_username(request, username):
    try:
        user = User.objects.get(username=username)
        settings = UserSettings.objects.get(user=user)

        if not settings.is_public:
            return Response({"error": "This user's schedule is private."}, status=403)

        entries = TimetableEntry.objects.filter(user=user)
        serializer = TimetableEntrySerializer(entries, many=True)
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    

@login_required
def calendar(request):
    username = request.user.username
    settings = UserSettings.objects.get(user=request.user)
    return render(request, "calendar.html", {"days": DAYS, "username": username, "settings": settings})


@login_required
def update_settings(request):
    settings = UserSettings.objects.get(user=request.user)
    if request.method == "POST":
        toggle_value = (request.POST.get("is_public", "off") == "on")
        settings.is_public = toggle_value
        settings.save()
        return redirect("calendar")


def calendar_guest(request, user):
    return render(request, "calendar.html", {"days": DAYS, "username": user, "is_guest": True})


