from rest_framework import permissions, viewsets
from core.serializers import CommunitySerializer
from core.models import Community

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]
