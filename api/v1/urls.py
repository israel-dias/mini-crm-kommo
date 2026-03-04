# api/v1/urls.py
from django.urls import include, path

urlpatterns = [
    path("", include("apps.organizations.urls")),  # mantém /me/organizations/
    path("", include("api.v1.routers")),
]
