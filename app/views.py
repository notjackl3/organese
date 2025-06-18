from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from .models import Timetable, TimetableEntry, BookingRequest
from .serializers import TimetableSerializer, TimetableEntrySerializer, BookingRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class TimetableEntryList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET request to retrieve timetable data
    def get(self, request):
        # get data from url query, search for the timetable, then retrieve entries of that timetable
        timetable_id = request.query_params.get('timetable_id')
        timetable = get_object_or_404(Timetable, id=timetable_id)
        entries = TimetableEntry.objects.filter(timetable=timetable)
        serializer = TimetableEntrySerializer(entries, many=True)
        return Response(serializer.data)

    # POST request to add new timetable data
    def post(self, request):
        # use serializer to standardize data, get timetable_id from request data body, search for the timetable then save entry of that table
        serializer = TimetableEntrySerializer(data=request.data)
        if serializer.is_valid():
            timetable_id = request.data.get('timetable_id')
            timetable = get_object_or_404(Timetable, id=timetable_id)
            serializer.save(timetable=timetable)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimetableEntryDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # PUT request is for replacing data
    def put(self, request, pk):
        entry = self.get_object(pk, request.user)
        serializer = TimetableEntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH request is for altering data
    def patch(self, request, pk):
        entry = self.get_object(pk, request.user)
        serializer = TimetableEntrySerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        entry = TimetableEntry.objects.get(id=pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TimetableEntryLookup(APIView):
    # get all data from request data body, then search for the table entry that has the matching timings and then return them
    def post(self, request):
        day = request.data.get('day_of_week')
        hour = request.data.get('hour')
        timetable_id = request.data.get('timetable_id')
        timetable = get_object_or_404(Timetable, id=timetable_id)
        try:
            entry = TimetableEntry.objects.get(
                day_of_week=day,
                hour=hour,
                timetable=timetable,
            )
            return Response({"pk": entry.pk}, status=status.HTTP_200_OK)
        except TimetableEntry.DoesNotExist:
            return Response({"error": "No entry found."}, status=status.HTTP_404_NOT_FOUND)
        except TimetableEntry.MultipleObjectsReturned:
            entries = TimetableEntry.objects.filter(
                day_of_week=day,
                hour=hour,
                timetable=timetable,
            )                       
            return Response({"multiple": True, "pk": list(entries.values())}, status=status.HTTP_200_OK)
        

class TimetableGuestEntryList(APIView):
    # allow anyone to access using the guest link
    permission_classes = [AllowAny]
    def get(self, request):
        # get timetable_id from query paraeter then retrieve all entries of that timetable
        try:
            timetable_id = request.query_params.get('timetable_id')
            timetable = get_object_or_404(Timetable, id=timetable_id)

            if not timetable.is_public:
                return Response({"error": "This user's schedule is private."}, status=403)

            entries = TimetableEntry.objects.filter(timetable=timetable)
            serializer = TimetableEntrySerializer(entries, many=True)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
    

class TimetableList(APIView):
    # get user_id from request data body then create a table. The name of the table will be included in request.data already, and it is serialized
    def post(self, request):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        serializer = TimetableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingRequestList(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        if serializer.is_valid():
            timetable_id = request.data.get('timetable_id')
            timetable = get_object_or_404(Timetable, id=timetable_id)
            user = timetable.user
            serializer.save(owner=user, timetable=timetable)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def home(request):
    username = User.objects.get(username=request.user.username)
    timetable = Timetable.objects.filter(user=username.id).first()
    timetable_name = timetable.name
    timetable_id = timetable.id
    is_public = timetable.is_public
    return render(request, "calendar.html", {
        "days": DAYS,
        "username": username,
        "timetable_id": timetable_id,
        "timetable_name": timetable_name,
        "is_public": is_public,
    })


@login_required
def calendar(request, timetable_name):
    username = request.user.username
    timetable = Timetable.objects.get(name=timetable_name)
    timetable_id = timetable.id
    is_public = timetable.is_public
    return render(request, "calendar.html", {
        "days": DAYS,
        "username": username,
        "timetable_id": timetable_id,
        "timetable_name": timetable_name,
        "is_public": is_public,
    })


@login_required
def update_settings(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    if request.method == "POST":
        toggle_value = (request.POST.get("is_public", "off") == "on")
        timetable.is_public = toggle_value
        timetable.save()
        return redirect("home")


def calendar_guest(request, username, timetable_name):
    timetable = Timetable.objects.get(name=timetable_name)
    timetable_id = timetable.id
    return render(request, "calendar.html", {
        "days": DAYS,
        "username": username,
        "timetable_id": timetable_id,
        "timetable_name": timetable_name,
        "is_guest": True
    })


def booking(request, username):
    user = User.objects.get(username=request.user.username)
    bookings = BookingRequest.objects.filter(owner=user, status="pending")
    return render(request, "bookings.html", {
        "bookings": bookings,
        "username": username})