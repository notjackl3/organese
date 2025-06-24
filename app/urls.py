from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # calendar view, for rendering the page
    path("", RedirectView.as_view(url="calendar/", permanent=False)),
    path("calendar/", views.home, name="home"),
    path("calendar/<str:timetable_name>/", views.calendar, name="calendar"),
    path("calendar-guest/<str:username>/<str:timetable_name>/", views.calendar_guest, name="calendar-guest"),
    # PUT, PATCH, DELETE
    path("entries/change/<int:pk>/", views.TimetableEntryDetail.as_view(), name="entry-change"),
    path("entries/lookup/", views.TimetableEntryLookup.as_view(), name="entry-lookup"),
    # GET, POST
    path("entries/", views.TimetableEntryList.as_view(), name="entries-list"),
    # guest's view
    path("entries-guest/", views.TimetableGuestEntryList.as_view(), name="entries-guest"),
    # update public permissions to the timetable
    path("update-settings/<int:id>", views.update_settings, name="update_settings"),
    path("table/", views.TimetableList.as_view(), name="manage-table"),
    # manage requests from guests
    path("booking/create/", views.BookingRequestList.as_view(), name="booking-create"),
    path("booking/change/", views.BookingEntryDetail.as_view(), name="booking-change"),
    path("booking/add/", views.BookingEntryList.as_view(), name="booking-add"),
    path("booking/<str:username>/", views.booking, name="booking"),
]
