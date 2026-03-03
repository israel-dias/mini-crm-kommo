import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.organizations.models import Organization, Membership
from apps.crm_pipelines.models import Pipeline, Stage


@pytest.mark.django_db
def test_tenant_isolation_pipelines_list_and_create():
    user = User.objects.create_user(username="u1", email="u1@mail.com", password="123456")

    org1 = Organization.objects.create(name="Org 1", slug="org-1")
    org2 = Organization.objects.create(name="Org 2", slug="org-2")

    Membership.objects.create(user=user, organization=org1, role=Membership.Role.ADMIN, is_active=True)

    client = APIClient()
    client.force_authenticate(user=user)

    # Criar pipeline na org1 (com header)
    res_create = client.post(
        "/api/v1/pipelines/",
        {"name": "Vendas", "is_default": True, "ordering": 1},
        format="json",
        HTTP_X_ORGANIZATION_ID=str(org1.id),
    )
    assert res_create.status_code == 201
    pipeline_id = res_create.json()["id"]

    # Criar pipeline diretamente na org2 (via ORM), só pra testar isolamento
    Pipeline.objects.create(organization=org2, name="Outro Funil", is_default=True, ordering=1)

    # Listar com header org1 -> deve ver só 1 (o da org1)
    res_list_org1 = client.get("/api/v1/pipelines/", HTTP_X_ORGANIZATION_ID=str(org1.id))
    assert res_list_org1.status_code == 200
    assert res_list_org1.json()["count"] == 1
    assert res_list_org1.json()["results"][0]["id"] == pipeline_id

    # Tentar listar com header org2 (sem membership) -> middleware bloqueia 403
    res_list_org2 = client.get("/api/v1/pipelines/", HTTP_X_ORGANIZATION_ID=str(org2.id))
    assert res_list_org2.status_code == 403


@pytest.mark.django_db
def test_cross_tenant_uuid_access_returns_404():
    user = User.objects.create_user(username="u1", email="u1@mail.com", password="123456")
    org1 = Organization.objects.create(name="Org 1", slug="org-1")
    org2 = Organization.objects.create(name="Org 2", slug="org-2")

    Membership.objects.create(user=user, organization=org1, role=Membership.Role.ADMIN, is_active=True)

    pipeline_org2 = Pipeline.objects.create(organization=org2, name="Org2 Funil", is_default=True, ordering=1)

    client = APIClient()
    client.force_authenticate(user=user)

    # Mesmo autenticado e com header org1, tentar pegar pipeline org2 por UUID -> 404
    res = client.get(f"/api/v1/pipelines/{pipeline_org2.id}/", HTTP_X_ORGANIZATION_ID=str(org1.id))
    assert res.status_code == 404


@pytest.mark.django_db
def test_tenant_scoped_endpoints_require_header():
    user = User.objects.create_user(username="u1", email="u1@mail.com", password="123456")
    org1 = Organization.objects.create(name="Org 1", slug="org-1")
    Membership.objects.create(user=user, organization=org1, role=Membership.Role.ADMIN, is_active=True)

    client = APIClient()
    client.force_authenticate(user=user)

    # Sem header -> permission HasActiveOrganization deve bloquear (403)
    res = client.get("/api/v1/pipelines/")
    assert res.status_code == 403
    assert "Active organization required" in res.json().get("detail", "")


@pytest.mark.django_db
def test_rbac_viewer_cannot_mutate_but_can_read():
    user = User.objects.create_user(username="viewer", email="viewer@mail.com", password="123456")
    org1 = Organization.objects.create(name="Org 1", slug="org-1")
    Membership.objects.create(user=user, organization=org1, role=Membership.Role.VIEWER, is_active=True)

    pipeline = Pipeline.objects.create(organization=org1, name="Vendas", is_default=True, ordering=1)

    client = APIClient()
    client.force_authenticate(user=user)

    # READ OK
    res_list = client.get("/api/v1/pipelines/", HTTP_X_ORGANIZATION_ID=str(org1.id))
    assert res_list.status_code == 200

    # MUTATE BLOCKED
    res_post = client.post(
        "/api/v1/pipelines/",
        {"name": "Novo", "is_default": False, "ordering": 2},
        format="json",
        HTTP_X_ORGANIZATION_ID=str(org1.id),
    )
    assert res_post.status_code == 403

    res_delete = client.delete(f"/api/v1/pipelines/{pipeline.id}/", HTTP_X_ORGANIZATION_ID=str(org1.id))
    assert res_delete.status_code == 403


@pytest.mark.django_db
def test_stage_validation_rejects_pipeline_from_other_org():
    admin = User.objects.create_user(username="admin", email="admin@mail.com", password="123456")

    org1 = Organization.objects.create(name="Org 1", slug="org-1")
    org2 = Organization.objects.create(name="Org 2", slug="org-2")
    Membership.objects.create(user=admin, organization=org1, role=Membership.Role.ADMIN, is_active=True)

    pipeline_org2 = Pipeline.objects.create(organization=org2, name="Org2 Funil", is_default=True, ordering=1)

    client = APIClient()
    client.force_authenticate(user=admin)

    # Tenta criar stage na org1 apontando pipeline da org2 -> 400 (serializer valida)
    res = client.post(
        "/api/v1/stages/",
        {"pipeline": str(pipeline_org2.id), "name": "Novo", "order": 1, "is_won": False, "is_lost": False},
        format="json",
        HTTP_X_ORGANIZATION_ID=str(org1.id),
    )
    assert res.status_code == 400
    assert "Pipeline does not belong to the active organization" in str(res.json())