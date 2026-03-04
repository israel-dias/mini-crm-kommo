# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.organizations.models import Membership
from apps.organizations.serializers import MembershipSerializer


class MyOrganizationsView(APIView):
    """
    Retorna as organizations que o usuário participa.
    Aqui NÃO precisa de X-Organization-ID, porque é a seleção de tenant.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        memberships = Membership.objects.filter(user=request.user, is_active=True).select_related(
            "organization"
        )
        data = MembershipSerializer(memberships, many=True).data
        return Response(data)
