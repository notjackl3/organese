from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='calendar/', permanent=False)),
    path("calendar/", views.home, name="home"),
    path("calendar/<str:timetable_name>/", views.calendar, name="calendar"),
    path("calendar-guest/<str:username>/<str:timetable_name>/", views.calendar_guest, name="calendar_guest"),
    # GET, PUT, PATCH, DELETE
    path('entries/<int:pk>/', views.TimetableEntryDetail.as_view(), name='entry-detail'),
    path('entries/lookup/', views.TimetableEntryLookup.as_view(), name='entry-lookup'),
    # GET, POST
    path('entries/', views.TimetableEntryList.as_view(), name='entry-list'),
    path("entries-guest/", views.TimetableGuestEntryList.as_view(), name="public_entries"),
    # update public permissions to the timetable
    path('update-settings/<int:id>', views.update_settings, name='update_settings'),
]
