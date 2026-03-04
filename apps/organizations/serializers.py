# Primeiro endpoint: listar minhas organizations (sem header)
from rest_framework import serializers

from apps.organizations.models import Membership, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug"]


class MembershipSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Membership
        fields = ["id", "role", "is_active", "organization"]
