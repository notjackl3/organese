from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import TimetableEntry
from .serializers import TimetableEntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404



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
        content = request.data.get('content')
        print(day)
        print(hour)
        print(content)
        # ERROR HERE IS MULTIPLE OBJECT BEING RETURN, HAVE TO FIX THAT AND ALSO ALLOWS USER TO ONLY INPUT ONCE. ALSO, TRY TO PREVENT ROWS WITH NULL CONTENT TO SAVE DATA
        try:
            entry = TimetableEntry.objects.get(
                day_of_week=day,
                hour=hour,
                content=content
            )
            return Response({"pk": entry.pk}, status=status.HTTP_200_OK)
        except TimetableEntry.DoesNotExist:
            return Response({"error": "No entry found."}, status=status.HTTP_404_NOT_FOUND)
        

@login_required
def home(request):
    return render(request, "index.html", {"days": DAYS})

