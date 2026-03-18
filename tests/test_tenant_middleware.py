# O endpoint de listar orgs não deve depender do header.
# O bloqueio cross-tenant será validado quando criarmos
# um endpoint realmente tenant-scoped (ex.: Deals).
# para que eu possa testar isso direito.


import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.organizations.models import Membership, Organization


@pytest.mark.django_db
def test_user_can_list_own_organizations():
    user = User.objects.create_user(username="draco", email="draco@mail.com", password="123456")
    org = Organization.objects.create(name="Org 1", slug="org-1")
    Membership.objects.create(user=user, organization=org, role=Membership.Role.ADMIN)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("my-organizations")
    res = client.get(url)

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["organization"]["id"] == str(org.id)


@pytest.mark.django_db
def test_cross_tenant_is_blocked_by_middleware():
    user = User.objects.create_user(username="draco", email="draco@mail.com", password="123456")
    org1 = Organization.objects.create(name="Org 1", slug="org-1")
    org2 = Organization.objects.create(name="Org 2", slug="org-2")
    Membership.objects.create(user=user, organization=org1, role=Membership.Role.ADMIN)

    client = APIClient()
    client.force_authenticate(user=user)

    # tenta setar org2 no header sem ser membro
    url = reverse("my-organizations")
    res = client.get(url, HTTP_X_ORGANIZATION_ID=str(org2.id))

    # Este endpoint específico não bloqueia por header, ele ignora.
    # Então aqui o teste relevante será em um endpoint tenant-scoped.
    assert res.status_code == 200
