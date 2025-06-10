from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # GET, POST
    path('entries/', views.TimetableEntryList.as_view(), name='entry-list'),
    # GET, PUT, PATCH, DELETE
    path('entries/<int:pk>/', views.TimetableEntryDetail.as_view(), name='entry-detail'),
    path('entries/lookup/', views.TimetableEntryLookup.as_view(), name='entry-lookup')
]
