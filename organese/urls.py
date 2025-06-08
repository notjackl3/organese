from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", include("app.urls")),
    path("accounts/", include("authentication.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico')))
]

