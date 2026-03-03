# apps/organizations/urls.py
from django.urls import path
from apps.organizations.views import MyOrganizationsView

urlpatterns = [
    path("me/organizations/", MyOrganizationsView.as_view(), name="my-organizations"),
]